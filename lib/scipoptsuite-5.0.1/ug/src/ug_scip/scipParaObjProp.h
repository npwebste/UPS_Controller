/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                           */
/*                  This file is part of the program and library             */
/*         SCIP --- Solving Constraint Integer Programs                      */
/*                                                                           */
/*    Copyright (C) 2002-2017 Konrad-Zuse-Zentrum                            */
/*                            fuer Informationstechnik Berlin                */
/*                                                                           */
/*  SCIP is distributed under the terms of the ZIB Academic License.         */
/*                                                                           */
/*  You should have received a copy of the ZIB Academic License.             */
/*  along with SCIP; see the file COPYING. If not email to scip@zib.de.      */
/*                                                                           */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**@file   scipParaObjProp.h
 * @brief  C++ wrapper for propagators
 * @author Yuji Shinano
 */

/*---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0----+----1----+----2*/

#ifndef __SCIP_PARA_OBJPROP_H__
#define __SCIP_PARA_OBJPROP_H__

#include <cstring>
#include <list>

#include "scipParaSolver.h"
#include "objscip/objprop.h"
#include "ug/paraComm.h"

namespace ParaSCIP
{

struct BoundChange{
   SCIP_BOUNDTYPE boundType;
   int            index;
   SCIP_Real      bound;
};

/** @brief C++ wrapper for propagators
 *
 *  This class defines the interface for propagators implemented in C++. Note that there is a pure virtual
 *  function (this function has to be implemented). This function is: scip_exec().
 *
 *  - \ref PROP "Instructions for implementing a propagator"
 *  - \ref PROPAGATORS "List of available propagators"
 *  - \ref type_prop.h "Corresponding C interface"
 */
class ScipParaObjProp : public scip::ObjProp
{
   // UG::ParaComm *paraComm;
   std::list<BoundChange *> boundChanges;
   int             ntotaltightened;
   int             ntotaltightenedint;
public:
   /** default constructor */
   ScipParaObjProp(
         UG::ParaComm   *comm,
         ScipParaSolver *solver
      ) : scip::ObjProp::ObjProp(
            solver->getScip(),
            "ScipParaObjProp",
            "Propagator for updating variable bounds",
            (INT_MAX/4),
            -1,
            0,
            SCIP_PROPTIMING_ALWAYS,
            (INT_MAX/4) ,
            -1,
            SCIP_PRESOLTIMING_FAST
            )// , paraComm(comm)
             , ntotaltightened(0), ntotaltightenedint(0)
   {
   }

   /** destructor */
   virtual ~ScipParaObjProp()
   {
      std::list<BoundChange *>::iterator it = boundChanges.begin();
      while( it != boundChanges.end() )
      {
         BoundChange *bc = boundChanges.front();
         it = boundChanges.erase(it);
         delete bc;
      }
   }

   /** execution method of propagator
    *
    *  @see SCIP_DECL_PROPEXEC(x) in @ref type_prop.h
    */
   SCIP_RETCODE applyBoundChanges(SCIP *scip, int& ntightened, int& ntightenedint, SCIP_RESULT *result )
   {
      // std::cout << "#### exec propagator ##### Rank = " << paraComm->getRank() << std::endl;
      ntightened = 0;
      ntightenedint = 0;

      *result = SCIP_DIDNOTFIND;

      std::list<BoundChange *>::iterator it = boundChanges.begin();
      while( it != boundChanges.end() )
      {
         BoundChange *bc = boundChanges.front();
         SCIP_Var **orgVars = SCIPgetOrigVars(scip);
         SCIP_Var *var = SCIPvarGetTransVar(orgVars[bc->index]);
         if ( *result != SCIP_CUTOFF && var && SCIPvarGetStatus(var) != SCIP_VARSTATUS_FIXED && SCIPvarGetStatus(var) != SCIP_VARSTATUS_MULTAGGR && SCIPvarGetStatus(var) != SCIP_VARSTATUS_AGGREGATED )  // Can recive bounds during presolving
         {
            if( SCIPvarGetStatus(var) == SCIP_VARSTATUS_NEGATED )
            {
               SCIP_Var *varNeg = 0;
               SCIP_CALL_ABORT ( SCIPgetNegatedVar(scip, var, &varNeg) );
               if( SCIPvarIsActive(varNeg) )
               {
                  SCIP_CALL( tryToTightenBound(scip, bc->boundType, orgVars[bc->index], bc->bound, result, ntightened, ntightenedint ) );
               }
            }
            else
            {
               SCIP_CALL( tryToTightenBound(scip, bc->boundType, orgVars[bc->index], bc->bound, result, ntightened, ntightenedint ) );
            }
         }
         it = boundChanges.erase(it);
         delete bc;
      }

      return SCIP_OKAY;
   }

   /** presolving method of propagator
       *
       *  @see SCIP_DECL_PROPPRESOL(x) in @ref type_prop.h
       */
   virtual SCIP_DECL_PROPPRESOL(scip_presol)
   {
      int             ntightened;
      int             ntightenedint;
      *result = SCIP_DIDNOTRUN;

      if( boundChanges.empty() || SCIPinProbing(scip) )
         return SCIP_OKAY;

      applyBoundChanges(scip, ntightened, ntightenedint, result);

      if( ntightened > 0 )
      {
         *nchgbds += ntightened;
         ntotaltightened += ntightened;
         ntotaltightenedint += ntightenedint;
         if( *result != SCIP_CUTOFF )
            *result = SCIP_SUCCESS;
         // std::cout << "$$$$$ tightened " << ntightened << " var bounds in Rank " << paraComm->getRank() << " of which " << ntightenedint << " where integral vars." << std::endl;
      }
      SCIPpropSetFreq(prop, -1);
      return SCIP_OKAY;
   }

   /** execution method of propagator
    *
    *  @see SCIP_DECL_PROPEXEC(x) in @ref type_prop.h
    */
   virtual SCIP_DECL_PROPEXEC(scip_exec)
   {
      // std::cout << "#### exec propagator ##### Rank = " << paraComm->getRank() << std::endl;
     int             ntightened;
     int             ntightenedint;
	  *result = SCIP_DIDNOTRUN;
	  
      if( SCIPinProbing(scip) )       
         return SCIP_OKAY;
	   
      applyBoundChanges(scip, ntightened, ntightenedint, result);
      
      if( ntightened > 0 )
      {
         ntotaltightened += ntightened;
         ntotaltightenedint += ntightenedint;
         if( *result != SCIP_CUTOFF )
            *result = SCIP_REDUCEDDOM;
         // std::cout << "$$$$$ tightened " << ntightened << " var bounds in Rank " << paraComm->getRank() << " of which " << ntightenedint << " where integral vars." << std::endl;
      }
      SCIPpropSetFreq(prop, -1);
      return SCIP_OKAY;
   }

   SCIP_RETCODE tryToTightenBound(SCIP *scip, SCIP_BOUNDTYPE boundType, SCIP_VAR *var, SCIP_Real bound, SCIP_Result *result, int& ntightened, int& ntightenedint )
   {
      SCIP_Bool infeas, tightened;
      if( boundType == SCIP_BOUNDTYPE_LOWER )
      {
         // std::cout << "### idx = " << bc->index << " Local lb = " << SCIPvarGetLbGlobal(orgVars[bc->index]) << ", bound = " << bc->bound << " #### Rank = " << paraComm->getRank() << std::endl;
         SCIP_CALL( SCIPtightenVarLbGlobal(scip, var, bound, FALSE, &infeas, &tightened) );
      }
      else
      {
         assert(boundType == SCIP_BOUNDTYPE_UPPER);
         // std::cout << "### idx = " << bc->index << " Local ub = " << SCIPvarGetUbGlobal(orgVars[bc->index]) << ", bound = " << bc->bound << " #### Rank = " << paraComm->getRank() << std::endl;
         SCIP_CALL( SCIPtightenVarUbGlobal(scip, var, bound, FALSE, &infeas, &tightened) );
      }
      // std::cout << "#### call SCIPtightenVarLbGlobal or SCIPtightenVarUbGlobal ##### Rank = " << paraComm->getRank()
      //     << ", infeas = " << infeas << ", tightened = " << tightened << std::endl;
      if( infeas )
      {
         ++ntightened;
         ++ntightenedint;
         *result = SCIP_CUTOFF;
         return SCIP_OKAY;
      }
      if( tightened )
      {
         ++ntightened;
         if( SCIPvarGetType(var) == SCIP_VARTYPE_BINARY
               || SCIPvarGetType(var) == SCIP_VARTYPE_INTEGER )
            ++ntightenedint;
      }
      return SCIP_OKAY;
   }

   void addBoundChange(SCIP *scip, SCIP_BOUNDTYPE boundType, int index, SCIP_Real bound)
   {
      BoundChange *bc = new BoundChange;
      bc->boundType = boundType;
      bc->index = index;
      bc->bound = bound;
      boundChanges.push_back(bc);
      SCIPsetIntParam(scip, "propagating/ScipParaObjProp/freq", 1);
   }

   int getNtightened(){ return ntotaltightened; }
   int getNtightenedInt(){ return ntotaltightenedint; }
};

} /* namespace ParaSCIP */

#endif // __SCIP_PARA_OBJPROP_H__
