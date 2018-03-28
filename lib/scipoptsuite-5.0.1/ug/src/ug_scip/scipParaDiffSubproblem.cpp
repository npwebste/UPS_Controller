/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                           */
/*             This file is part of the program and software framework       */
/*                  UG --- Ubquity Generator Framework                       */
/*                                                                           */
/*    Copyright (C) 2002-2017 Konrad-Zuse-Zentrum                            */
/*                            fuer Informationstechnik Berlin                */
/*                                                                           */
/*  UG is distributed under the terms of the ZIB Academic Licence.           */
/*                                                                           */
/*  You should have received a copy of the ZIB Academic License              */
/*  along with UG; see the file COPYING. If not email to scip@zib.de.        */
/*                                                                           */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**@file    scipParaDiffSubproblem.cpp
 * @brief   ParaDiffSubproblem extension for SCIP solver.
 * @author  Yuji Shinano
 *
 *
 *
 */

/*---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0----+----1----+----2*/


#include "ug/paraComm.h"
#include "scipParaSolver.h"
#include "scipParaInstance.h"
#include "scipParaDiffSubproblem.h"
#include "scipParaInitiator.h"

using namespace UG;
using namespace ParaSCIP;

ScipParaDiffSubproblem::ScipParaDiffSubproblem(
      SCIP *scip,
      ScipParaSolver *scipParaSolver,
      int nNewBranchVars,
      SCIP_VAR **newBranchVars,
      SCIP_Real *newBranchBounds,
      SCIP_BOUNDTYPE *newBoundTypes
      ) :   localInfoIncluded(0),
            nBoundChanges(0), indicesAmongSolvers(0), branchBounds(0), boundTypes(0),
            linearConss(0),
            boundDisjunctions(0),
            varBranchStats(0),
            varValues(0)
{
   // int nOrigVars = SCIPgetNOrigVars(scip);
   // std::cout << "the number of original variables = " << nOrigVars << std::endl;

   nBoundChanges = nNewBranchVars;
   int nParentBranchVars = 0;
   int i = 0;

   ScipParaDiffSubproblem *parentDiffSubproblem = scipParaSolver->getParentDiffSubproblem();

   if( parentDiffSubproblem )
   {
      nParentBranchVars = parentDiffSubproblem->getNBoundChanges();
      nBoundChanges += nParentBranchVars;
   }
   indicesAmongSolvers = new int[nBoundChanges];
   branchBounds = new SCIP_Real[nBoundChanges];
   boundTypes = new SCIP_BOUNDTYPE[nBoundChanges];
   if( parentDiffSubproblem )
   {
      for( i = 0; i < nParentBranchVars; i ++ )
      {
         indicesAmongSolvers[i] = parentDiffSubproblem->getIndex(i);
         branchBounds[i] = parentDiffSubproblem->getBranchBound(i);
         boundTypes[i] = parentDiffSubproblem->getBoundType(i);
      }
   }

   for( int v = nNewBranchVars -1 ; v >= 0; --v )
   {
      SCIP_VAR *transformVar = newBranchVars[v];
      SCIP_Real scalar = 1.0;
      SCIP_Real constant = 0.0;
      SCIP_CALL_ABORT( SCIPvarGetOrigvarSum(&transformVar, &scalar, &constant ) );
      if( transformVar == NULL ) continue;
      assert( (!scipParaSolver->getParaParamSet()->getBoolParamValue(NoSolverPresolvingAtRoot) ) ||
              (!scipParaSolver->getCurrentNode()->isRootNode() ) ||
              ( scipParaSolver->getParaParamSet()->getBoolParamValue(NoSolverPresolvingAtRoot)  &&
                  scipParaSolver->getCurrentNode()->isRootNode() &&
                  scalar == 1.0 && constant == 0.0 )
            );
      if( scipParaSolver->isOriginalIndeciesMap() )
      {
         indicesAmongSolvers[i] = scipParaSolver->getOriginalIndex(SCIPvarGetIndex(transformVar));
      }
      else
      {
         indicesAmongSolvers[i] = SCIPvarGetIndex(transformVar);
      }
      // assert(indicesAmongSolvers[i] < nOrigVars);
      branchBounds[i] = ( newBranchBounds[v] - constant ) / scalar;
      if( scalar > 0.0 )
      {
         boundTypes[i] = newBoundTypes[v];
      }
      else
      {
         boundTypes[i] = SCIP_BoundType(1 - newBoundTypes[v]);
      }
      if( SCIPvarGetType(transformVar) != SCIP_VARTYPE_CONTINUOUS )
      {
         if( boundTypes[i] == SCIP_BOUNDTYPE_LOWER )
         {
            branchBounds[i] = SCIPfeasCeil(scip, branchBounds[i]);
            // this does not work in case of multi-aggregated 
            // assert( scipParaSolver->getOrgVarLb(indicesAmongSolvers[i]) <=  branchBounds[i] );
         }
         else
         {
            branchBounds[i] = SCIPfeasFloor(scip, branchBounds[i]);
            // this does not work in case of multi-aggregated 
            // assert( scipParaSolver->getOrgVarUb(indicesAmongSolvers[i]) >=  branchBounds[i] );
         }
      }
      // This does not work in case of multi-aggregated 
      // std::cout << scipParaSolver->getOrgVarLb(indicesAmongSolvers[i]) << " <= "
      //       <<  branchBounds[i] << " <= "
      //       <<  scipParaSolver->getOrgVarUb(indicesAmongSolvers[i]) << std::endl;
      assert( SCIPisLE(scip,scipParaSolver->getOrgVarLb(SCIPvarGetProbindex(transformVar)), branchBounds[i]) &&
             SCIPisGE(scip,scipParaSolver->getOrgVarUb(SCIPvarGetProbindex(transformVar)), branchBounds[i]) );
      assert( SCIPvarGetType(transformVar) !=  SCIP_VARTYPE_BINARY ||
             ( SCIPvarGetType(transformVar) == SCIP_VARTYPE_BINARY && boundTypes[i] == SCIP_BOUNDTYPE_LOWER && EPSEQ(branchBounds[i], 1.0, DEFAULT_NUM_EPSILON ) ) ||
             ( SCIPvarGetType(transformVar) == SCIP_VARTYPE_BINARY && boundTypes[i] == SCIP_BOUNDTYPE_UPPER && EPSEQ(branchBounds[i], 0.0, DEFAULT_NUM_EPSILON ) ) );
      i++;
   }
   nBoundChanges = i;

   if( scipParaSolver->getParaParamSet()->getBoolParamValue(TransferLocalCuts) ||
         scipParaSolver->getParaParamSet()->getBoolParamValue(TransferConflictCuts)
         )
   {
      addLocalNodeInfo(scip, scipParaSolver);
   }

   if( scipParaSolver->getParaParamSet()->getBoolParamValue(TransferConflicts) )
   {
      addBoundDisjunctions(scip, scipParaSolver);
   }

   if( scipParaSolver->getParaParamSet()->getBoolParamValue(TransferBranchStats) &&
         (!( scipParaSolver->isRacingStage()
               && scipParaSolver->getParaParamSet()->getBoolParamValue(RacingStatBranching) ) )
         )
   {
      addBranchVarStats(scip, scipParaSolver);
   }

   if( scipParaSolver->getParaParamSet()->getBoolParamValue(TransferVarValueStats) &&
         (!( scipParaSolver->isRacingStage()
               && scipParaSolver->getParaParamSet()->getBoolParamValue(RacingStatBranching) ) )
         )
   {
      addVarValueStats(scip, scipParaSolver);
   }
#ifdef UG_DEBUG_SOLUTION
   includeOptimalSol = 0;
#endif
}

void
ScipParaDiffSubproblem::addLocalNodeInfo(
      SCIP *scip,
      ScipParaSolver *scipParaSolver
      )
{
   std::list<LocalNodeInfoPtr> localCutsList;

   if( scipParaSolver->getParaParamSet()->getBoolParamValue(TransferLocalCuts) )
   {
      SCIP_CUT** cuts;
      int ncuts;

      cuts = SCIPgetPoolCuts(scip);
      ncuts = SCIPgetNPoolCuts(scip);

      for( int c = 0; c < ncuts; ++c )
      {
         SCIP_ROW* row;

         row = SCIPcutGetRow(cuts[c]);
         assert(!SCIProwIsLocal(row));
         assert(!SCIProwIsModifiable(row));
         if( SCIPcutGetAge(cuts[c]) == 0 && SCIProwIsInLP(row) )
         {
            SCIP_COL** cols;
            int ncols;
            int i;

            /* create a linear constraint out of the cut */
            cols = SCIProwGetCols(row);
            ncols = SCIProwGetNNonz(row);

            LocalNodeInfo *localNodeInfo = new LocalNodeInfo;
            localNodeInfo->nLinearCoefs = ncols;
            localNodeInfo->idxLinearCoefsVars = new int[ncols];
            localNodeInfo->linearCoefs = new double[ncols];
            double lhs, rhs;
            if( !SCIPisInfinity(scip, -SCIProwGetLhs(row)) )
            {
               lhs = SCIProwGetLhs(row) - SCIProwGetConstant(row);
            }
            else
            {
               lhs = -SCIPinfinity(scip);
            }
            if( !SCIPisInfinity(scip, SCIProwGetRhs(row)) )
            {
               rhs = SCIProwGetRhs(row) - SCIProwGetConstant(row);
            }
            else
            {
               rhs = SCIPinfinity(scip);
            }

            SCIP_Real *vals = SCIProwGetVals(row);
            for( i = 0; i < ncols; ++i )
            {
               SCIP_VAR *transformVar = SCIPcolGetVar(cols[i]);
               SCIP_Real scalar = vals[i];
               SCIP_Real constant = 0.0;
               if( SCIPvarGetOrigvarSum(&transformVar, &scalar, &constant ) ==  SCIP_INVALIDDATA )
                  break;
               if( transformVar == NULL )
                  break;
               // assert(transformVar != NULL);
               if( !SCIPisInfinity(scip, -SCIProwGetLhs(row)) )
               {
                  lhs -= constant;
               }
               if( !SCIPisInfinity(scip, SCIProwGetRhs(row)) )
               {
                  rhs -= constant;
               }
               if( scipParaSolver->isOriginalIndeciesMap() )
               {
                  localNodeInfo->idxLinearCoefsVars[i] = scipParaSolver->getOriginalIndex(SCIPvarGetIndex(transformVar));
               }
               else
               {
                  localNodeInfo->idxLinearCoefsVars[i] = SCIPvarGetIndex(transformVar);
               }
               localNodeInfo->linearCoefs[i] = scalar;
            }
            if( i == ncols )
            {
               assert( !SCIPisInfinity(scip, -SCIProwGetLhs(row)) == !SCIPisInfinity(scip, -lhs)  );
               assert( !SCIPisInfinity(scip, SCIProwGetRhs(row)) == !SCIPisInfinity(scip, rhs)  );
               localNodeInfo->linearLhs = lhs;
               localNodeInfo->linearRhs = rhs;
               localCutsList.push_back(localNodeInfo);
            }
            else
            {
               delete [] localNodeInfo->idxLinearCoefsVars;
               delete [] localNodeInfo->linearCoefs;
               delete localNodeInfo;
            }
         }
      }
   }

   ScipParaDiffSubproblem *parentDiffSubproblem = scipParaSolver->getParentDiffSubproblem();
   std::list<LocalNodeInfoPtr> *conflictConsList = scipParaSolver->getConflictConsList();

   int nParentConss = 0;
   if( parentDiffSubproblem && parentDiffSubproblem->linearConss ) 
   {
      nParentConss +=  parentDiffSubproblem->linearConss->nLinearConss;
   }
   int nConflicts = 0;
   if( conflictConsList ) nConflicts += conflictConsList->size();
   if( nParentConss > 0 || nConflicts > 0 || localCutsList.size() > 0 )
   {
      linearConss = new ScipParaDiffSubproblemLinearCons();
      linearConss->nLinearConss = nParentConss + localCutsList.size() + nConflicts;
      scipParaSolver->updateNTransferredLocalCuts(linearConss->nLinearConss);
      if( linearConss->nLinearConss > 0 )
      {
         linearConss->linearLhss = new SCIP_Real[linearConss->nLinearConss];
         linearConss->linearRhss = new SCIP_Real[linearConss->nLinearConss];
         linearConss->nLinearCoefs = new int[linearConss->nLinearConss];
         linearConss->linearCoefs = new SCIP_Real*[linearConss->nLinearConss];
         linearConss->idxLinearCoefsVars = new int*[linearConss->nLinearConss];

         int i = 0;
         for(; i < nParentConss; i++ )
         {
            linearConss->linearLhss[i] = parentDiffSubproblem->linearConss->linearLhss[i];
            linearConss->linearRhss[i] = parentDiffSubproblem->linearConss->linearRhss[i];
            linearConss->nLinearCoefs[i] = parentDiffSubproblem->linearConss->nLinearCoefs[i];
            linearConss->linearCoefs[i] = new SCIP_Real[linearConss->nLinearCoefs[i]];
            linearConss->idxLinearCoefsVars[i] = new int[linearConss->nLinearCoefs[i]];
            for( int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
            {
               linearConss->linearCoefs[i][j] = parentDiffSubproblem->linearConss->linearCoefs[i][j];
               linearConss->idxLinearCoefsVars[i][j] = parentDiffSubproblem->linearConss->idxLinearCoefsVars[i][j];
            }
         }

         int nLocalCuts = localCutsList.size();
         for(; i < ( nParentConss + nLocalCuts ); i++ )
         {
            assert(!localCutsList.empty());
            LocalNodeInfo *cutInfo = localCutsList.front();
            localCutsList.pop_front();
            linearConss->linearLhss[i] = cutInfo->linearLhs;
            linearConss->linearRhss[i] = cutInfo->linearRhs;
            linearConss->nLinearCoefs[i] = cutInfo->nLinearCoefs;
            linearConss->linearCoefs[i] = cutInfo->linearCoefs;
            linearConss->idxLinearCoefsVars[i] = cutInfo->idxLinearCoefsVars;
            delete cutInfo;
         }

         if( i < linearConss->nLinearConss )
         {
            assert( conflictConsList );
            std::list<LocalNodeInfoPtr>::iterator pos;
            pos = conflictConsList->begin();
            for(; i < linearConss->nLinearConss; i++ )
            {
               assert( pos != conflictConsList->end() );
               linearConss->linearLhss[i] = (*pos)->linearLhs;
               linearConss->linearRhss[i] = (*pos)->linearRhs;
               linearConss->nLinearCoefs[i] = (*pos)->nLinearCoefs;
               linearConss->linearCoefs[i] = new SCIP_Real[linearConss->nLinearCoefs[i]];
               linearConss->idxLinearCoefsVars[i] = new int[linearConss->nLinearCoefs[i]];
               for( int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
               {
                  linearConss->linearCoefs[i][j] = (*pos)->linearCoefs[j];
                  linearConss->idxLinearCoefsVars[i][j] = (*pos)->idxLinearCoefsVars[j];
               }
               pos++;
            }
         }
      }
   }
}

void
ScipParaDiffSubproblem::addBoundDisjunctions(
      SCIP *scip,
      ScipParaSolver *scipParaSolver
      )
{
   boundDisjunctions = new ScipParaDiffSubproblemBoundDisjunctions();
   boundDisjunctions->nBoundDisjunctions = 0;
   for( int i = 0; i < SCIPgetNConshdlrs(scip); ++i )
   {
      SCIP_CONSHDLR* conshdlr = SCIPgetConshdlrs(scip)[i];
      int nactiveconss = SCIPconshdlrGetNActiveConss(conshdlr);
      if( nactiveconss > 0
          && std::string(SCIPconshdlrGetName(conshdlr)) == std::string("bounddisjunction") )
      {
         boundDisjunctions->nBoundDisjunctions = nactiveconss;
         SCIP_CONS **conss = SCIPconshdlrGetConss(conshdlr);
         boundDisjunctions->nVarsBoundDisjunction = new int[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionInitial = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionSeparate = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionEnforce = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionCheck = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionPropagate = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionLocal = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionModifiable = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionDynamic = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionRemovable = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionStickingatnode = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->idxBoundDisjunctionVars = new int*[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->boundTypesBoundDisjunction = new SCIP_BOUNDTYPE*[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->boundsBoundDisjunction = new SCIP_Real*[boundDisjunctions->nBoundDisjunctions];
         int nConss = 0;
         int nTotalVars = 0;
         for( int c = 0; c < nactiveconss; c++ )
         {
            boundDisjunctions->nVarsBoundDisjunction[nConss] = SCIPgetNVarsBounddisjunction (scip, conss[c]);
            boundDisjunctions->flagBoundDisjunctionInitial[nConss] = SCIPconsIsInitial(conss[c]);
            boundDisjunctions->flagBoundDisjunctionSeparate[nConss] = SCIPconsIsSeparated(conss[c]);
            boundDisjunctions->flagBoundDisjunctionEnforce[nConss] = SCIPconsIsEnforced(conss[c]);
            boundDisjunctions->flagBoundDisjunctionCheck[nConss] = SCIPconsIsChecked(conss[c]);
            boundDisjunctions->flagBoundDisjunctionPropagate[nConss] = SCIPconsIsPropagated(conss[c]);
            boundDisjunctions->flagBoundDisjunctionLocal[nConss] = SCIPconsIsLocal(conss[c]);
            boundDisjunctions->flagBoundDisjunctionModifiable[nConss] = SCIPconsIsModifiable(conss[c]);
            boundDisjunctions->flagBoundDisjunctionDynamic[nConss] = SCIPconsIsDynamic(conss[c]);
            boundDisjunctions->flagBoundDisjunctionRemovable[nConss] = SCIPconsIsRemovable(conss[c]);
            boundDisjunctions->flagBoundDisjunctionStickingatnode[nConss] =SCIPconsIsStickingAtNode(conss[c]);
            if( boundDisjunctions->nVarsBoundDisjunction[nConss] > 0 )
            {
               boundDisjunctions->idxBoundDisjunctionVars[nConss] = new int[boundDisjunctions->nVarsBoundDisjunction[nConss]];
               boundDisjunctions->boundTypesBoundDisjunction[nConss] = new SCIP_BOUNDTYPE[boundDisjunctions->nVarsBoundDisjunction[nConss]];
               boundDisjunctions->boundsBoundDisjunction[nConss] = new SCIP_Real[boundDisjunctions->nVarsBoundDisjunction[nConss]];
               int v = 0;
               for( ; v < boundDisjunctions->nVarsBoundDisjunction[nConss]; v++ )
               {
                  SCIP_Var **vars = SCIPgetVarsBounddisjunction(scip, conss[c]);
                  SCIP_BOUNDTYPE *types = SCIPgetBoundtypesBounddisjunction(scip, conss[c]);
                  SCIP_Real *bounds = SCIPgetBoundsBounddisjunction(scip, conss[c]);

                  SCIP_VAR *transformVar = vars[v];
                  SCIP_Real scalar = 1.0;
                  SCIP_Real constant = 0.0;
                  SCIP_CALL_ABORT( SCIPvarGetOrigvarSum(&transformVar, &scalar, &constant ) );
                  if( transformVar )
                  {
                     if( scipParaSolver->isOriginalIndeciesMap( ))
                     {
                        boundDisjunctions->idxBoundDisjunctionVars[nConss][v] = scipParaSolver->getOriginalIndex(SCIPvarGetIndex(transformVar));
                     }
                     else
                     {
                        boundDisjunctions->idxBoundDisjunctionVars[nConss][v] = SCIPvarGetIndex(transformVar);
                     }
                     boundDisjunctions->boundTypesBoundDisjunction[nConss][v] = types[v];
                     boundDisjunctions->boundsBoundDisjunction[nConss][v] = bounds[v];
                     nTotalVars++;
                  }
                  else
                  {
                     break;
                  }
               }
               if( v == boundDisjunctions->nVarsBoundDisjunction[nConss] )
               {
                  nConss++;
               }
               else
               {
                  delete [] boundDisjunctions->boundsBoundDisjunction[nConss];
                  delete [] boundDisjunctions->boundTypesBoundDisjunction[nConss];
                  delete [] boundDisjunctions->idxBoundDisjunctionVars[nConss];
               }
            }
         }
         boundDisjunctions->nBoundDisjunctions = nConss;
         boundDisjunctions->nTotalVarsBoundDisjunctions = nTotalVars;
      }
   }
   if( boundDisjunctions->nBoundDisjunctions == 0 )
   {
      delete boundDisjunctions;
      boundDisjunctions = 0;
   }
}

void
ScipParaDiffSubproblem::addBranchVarStats(
      SCIP *scip,
      ScipParaSolver *scipParaSolver
      )
{
   int nvars;                                /* number of variables                           */
   int nbinvars;                             /* number of binary variables                    */
   int nintvars;                             /* number of integer variables                   */
   SCIP_VAR** vars;                          /* transformed problem's variables               */
   SCIP_CALL_ABORT( SCIPgetVarsData(scip, &vars, &nvars, &nbinvars, &nintvars, NULL, NULL) );
   int ngenvars = nbinvars+nintvars;
   varBranchStats = new ScipParaDiffSubproblemVarBranchStats();
   varBranchStats->idxBranchStatsVars = new int[ngenvars];
   varBranchStats->downpscost = new SCIP_Real[ngenvars];
   varBranchStats->uppscost = new SCIP_Real[ngenvars];
   varBranchStats->downvsids = new SCIP_Real[ngenvars];
   varBranchStats->upvsids = new SCIP_Real[ngenvars];
   varBranchStats->downconflen = new SCIP_Real[ngenvars];
   varBranchStats->upconflen = new SCIP_Real[ngenvars];
   varBranchStats->downinfer = new SCIP_Real[ngenvars];
   varBranchStats->upinfer = new SCIP_Real[ngenvars];
   varBranchStats->downcutoff = new SCIP_Real[ngenvars];
   varBranchStats->upcutoff = new SCIP_Real[ngenvars];
   int nOrgVars = 0;
   for( int i = 0; i < ngenvars; ++i )
   {
      assert( SCIPvarGetType(vars[i]) == SCIP_VARTYPE_BINARY || SCIPvarGetType(vars[i]) == SCIP_VARTYPE_INTEGER );
      SCIP_VAR *transformVar = vars[i];
      SCIP_Real scalar = 1.0;
      SCIP_Real constant = 0.0;
      SCIP_CALL_ABORT( SCIPvarGetOrigvarSum(&transformVar, &scalar, &constant ) );
      // assert(transformVar != NULL);
      if( transformVar )  // The variable in the transformed space
      {
         if( scipParaSolver->isOriginalIndeciesMap() )
         {
            varBranchStats->idxBranchStatsVars[nOrgVars] = scipParaSolver->getOriginalIndex(SCIPvarGetIndex(transformVar));
         }
         else
         {
            varBranchStats->idxBranchStatsVars[nOrgVars] = SCIPvarGetIndex(transformVar);
         }

         SCIP_BRANCHDIR branchdir1;
         SCIP_BRANCHDIR branchdir2;
         if( scalar > 0.0 )
         {
            branchdir1 = SCIP_BRANCHDIR_DOWNWARDS;
            branchdir2 = SCIP_BRANCHDIR_UPWARDS;
         }
         else
         {
            branchdir1 = SCIP_BRANCHDIR_UPWARDS;
            branchdir2 = SCIP_BRANCHDIR_DOWNWARDS;
         }
         varBranchStats->downpscost[nOrgVars] = SCIPgetVarPseudocost(scip, vars[i], branchdir1);
         varBranchStats->uppscost[nOrgVars] = SCIPgetVarPseudocost(scip, vars[i], branchdir2);
         varBranchStats->downvsids[nOrgVars] = SCIPgetVarVSIDS(scip, vars[i], branchdir1);
         varBranchStats->upvsids[nOrgVars] = SCIPgetVarVSIDS(scip, vars[i], branchdir2);
         varBranchStats->downconflen[nOrgVars] = SCIPgetVarAvgConflictlength(scip, vars[i], branchdir1);
         varBranchStats->upconflen[nOrgVars] = SCIPgetVarAvgConflictlength(scip, vars[i], branchdir2);
         varBranchStats->downinfer[nOrgVars] = SCIPgetVarAvgInferences(scip, vars[i], branchdir1);
         varBranchStats->upinfer[nOrgVars] = SCIPgetVarAvgInferences(scip, vars[i], branchdir2);
         varBranchStats->downcutoff[nOrgVars] = SCIPgetVarAvgCutoffs(scip, vars[i], branchdir1);
         varBranchStats->upcutoff[nOrgVars] = SCIPgetVarAvgCutoffs(scip, vars[i], branchdir2);
         nOrgVars++;
      }
   }
   // assert( nOrgVars == scipParaSolver->getNOrgVars() ); This is true.
   varBranchStats->nVarBranchStats = nOrgVars;
}

void
ScipParaDiffSubproblem::addVarValueStats(
      SCIP *scip,
      ScipParaSolver *scipParaSolver
      )
{
   int nvars;                                /* number of variables                           */
   int nbinvars;                             /* number of binary variables                    */
   int nintvars;                             /* number of integer variables                   */
   SCIP_VAR** vars;                          /* transformed problem's variables               */
   SCIP_CALL_ABORT( SCIPgetVarsData(scip, &vars, &nvars, &nbinvars, &nintvars, NULL, NULL) );
   int ngenvars = nbinvars+nintvars;

   varValues = new ScipParaDiffSubproblemVarValues();

   varValues->nVarValueVars = 0;
   varValues->nVarValues = 0;

   if( ngenvars > 0 )
   {
      varValues->idxVarValueVars = new int[ngenvars];
      varValues->nVarValueValues = new int[ngenvars];

      varValues->varValue            = new SCIP_Real*[ngenvars];
      varValues->varValueDownvsids   = new SCIP_Real*[ngenvars];
      varValues->varVlaueUpvsids     = new SCIP_Real*[ngenvars];
      varValues->varValueDownconflen = new SCIP_Real*[ngenvars];
      varValues->varValueUpconflen   = new SCIP_Real*[ngenvars];
      varValues->varValueDowninfer   = new SCIP_Real*[ngenvars];
      varValues->varValueUpinfer     = new SCIP_Real*[ngenvars];
      varValues->varValueDowncutoff  = new SCIP_Real*[ngenvars];
      varValues->varValueUpcutoff    = new SCIP_Real*[ngenvars];


      for( int i = 0; i < ngenvars; i++ )
      {
         assert( SCIPvarGetType(vars[i]) == SCIP_VARTYPE_BINARY || SCIPvarGetType(vars[i]) == SCIP_VARTYPE_INTEGER );

         SCIP_VAR *transformVar = vars[i];
         SCIP_Real scalar = 1.0;
         SCIP_Real constant = 0.0;
         SCIP_CALL_ABORT( SCIPvarGetOrigvarSum(&transformVar, &scalar, &constant ) );
         // assert(transformVar != NULL);

         if( transformVar )  // The variable in the transformed space
         {
            SCIP_VALUEHISTORY* valuehistory = SCIPvarGetValuehistory(vars[i]);
            if( valuehistory != NULL )
            {
               SCIP_HISTORY** histories;
               SCIP_Real* values;

               histories = SCIPvaluehistoryGetHistories(valuehistory);
               values = SCIPvaluehistoryGetValues(valuehistory);

               if( scipParaSolver->isOriginalIndeciesMap() )
               {
                  varValues->idxVarValueVars[varValues->nVarValueVars] = scipParaSolver->getOriginalIndex(SCIPvarGetIndex(transformVar));
               }
               else
               {
                  varValues->idxVarValueVars[varValues->nVarValueVars] = SCIPvarGetIndex(transformVar);
               }
               varValues->nVarValueValues[varValues->nVarValueVars] = SCIPvaluehistoryGetNValues(valuehistory);

               if( varValues->nVarValueValues[varValues->nVarValueVars] > 0 )
               {
                  varValues->varValue[varValues->nVarValueVars]            = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueDownvsids[varValues->nVarValueVars]   = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varVlaueUpvsids[varValues->nVarValueVars]     = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueDownconflen[varValues->nVarValueVars] = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueUpconflen[varValues->nVarValueVars]   = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueDowninfer[varValues->nVarValueVars]   = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueUpinfer[varValues->nVarValueVars]     = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueDowncutoff[varValues->nVarValueVars]  = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  varValues->varValueUpcutoff[varValues->nVarValueVars]    = new SCIP_Real[varValues->nVarValueValues[varValues->nVarValueVars]];
                  for( int j = 0; j < varValues->nVarValueValues[varValues->nVarValueVars]; j++ )
                  {
                     varValues->varValue[varValues->nVarValueVars][j]            = values[j];
                     varValues->varValueDownvsids[varValues->nVarValueVars][j]   = SCIPhistoryGetVSIDS( histories[j], SCIP_BRANCHDIR_DOWNWARDS );
                     varValues->varVlaueUpvsids[varValues->nVarValueVars][j]     = SCIPhistoryGetVSIDS( histories[j], SCIP_BRANCHDIR_UPWARDS );
                     varValues->varValueDownconflen[varValues->nVarValueVars][j] = SCIPhistoryGetAvgConflictlength( histories[j], SCIP_BRANCHDIR_DOWNWARDS );
                     varValues->varValueUpconflen[varValues->nVarValueVars][j]   = SCIPhistoryGetAvgConflictlength( histories[j], SCIP_BRANCHDIR_UPWARDS );
                     varValues->varValueDowninfer[varValues->nVarValueVars][j]   = SCIPhistoryGetInferenceSum( histories[j], SCIP_BRANCHDIR_DOWNWARDS );
                     varValues->varValueUpinfer[varValues->nVarValueVars][j]     = SCIPhistoryGetInferenceSum( histories[j], SCIP_BRANCHDIR_UPWARDS );
                     varValues->varValueDowncutoff[varValues->nVarValueVars][j]  = SCIPhistoryGetCutoffSum( histories[j], SCIP_BRANCHDIR_DOWNWARDS );
                     varValues->varValueUpcutoff[varValues->nVarValueVars][j]    = SCIPhistoryGetCutoffSum( histories[j], SCIP_BRANCHDIR_UPWARDS );
                     varValues->nVarValues++;
                  }
               }
               varValues->nVarValueVars++;
            }
         }
      }
   }
   if( varValues->nVarValueVars == 0 )
   {
      delete varValues;
      varValues = 0;
   }
}

void
ScipParaDiffSubproblem::addInitialBranchVarStats(
      int  inMinDepth,
      int  inMaxDepth,
      SCIP *scip
      )
{
   if( varBranchStats ) return;       /* if this is not initial transfer to the other solvers, do nothing */

   varBranchStats = new ScipParaDiffSubproblemVarBranchStats();
   varBranchStats->offset = inMinDepth;

   int nvars;                                /* number of variables                           */
   int nbinvars;                             /* number of binary variables                    */
   int nintvars;                             /* number of integer variables                   */
   SCIP_VAR** vars;                          /* transformed problem's variables               */
   SCIP_CALL_ABORT( SCIPgetVarsData(scip, &vars, &nvars, &nbinvars, &nintvars, NULL, NULL) );
   int ngenvars = nbinvars+nintvars;
   varBranchStats->nVarBranchStats = ngenvars;
   varBranchStats->idxBranchStatsVars = new int[ngenvars];
   varBranchStats->downpscost = new SCIP_Real[ngenvars];
   varBranchStats->uppscost = new SCIP_Real[ngenvars];
   varBranchStats->downvsids = new SCIP_Real[ngenvars];
   varBranchStats->upvsids = new SCIP_Real[ngenvars];
   varBranchStats->downconflen = new SCIP_Real[ngenvars];
   varBranchStats->upconflen = new SCIP_Real[ngenvars];
   varBranchStats->downinfer = new SCIP_Real[ngenvars];
   varBranchStats->upinfer = new SCIP_Real[ngenvars];
   varBranchStats->downcutoff = new SCIP_Real[ngenvars];
   varBranchStats->upcutoff = new SCIP_Real[ngenvars];
   for( int i = 0; i < ngenvars; ++i )
   {
      assert( SCIPvarGetType(vars[i]) == SCIP_VARTYPE_BINARY || SCIPvarGetType(vars[i]) == SCIP_VARTYPE_INTEGER );
      varBranchStats->idxBranchStatsVars[i] = SCIPvarGetProbindex(vars[i]);
      varBranchStats->downpscost[i] = SCIPgetVarPseudocost(scip, vars[i], SCIP_BRANCHDIR_DOWNWARDS);
      varBranchStats->uppscost[i] = SCIPgetVarPseudocost(scip, vars[i], SCIP_BRANCHDIR_UPWARDS);
      varBranchStats->downvsids[i] = SCIPgetVarVSIDS(scip, vars[i], SCIP_BRANCHDIR_DOWNWARDS);
      varBranchStats->upvsids[i] = SCIPgetVarVSIDS(scip, vars[i], SCIP_BRANCHDIR_UPWARDS);
      varBranchStats->downconflen[i] = SCIPgetVarAvgConflictlength(scip, vars[i], SCIP_BRANCHDIR_DOWNWARDS);
      varBranchStats->upconflen[i] = SCIPgetVarAvgConflictlength(scip, vars[i], SCIP_BRANCHDIR_UPWARDS);
      varBranchStats->downinfer[i] = SCIPgetVarAvgInferences(scip, vars[i], SCIP_BRANCHDIR_DOWNWARDS);
      varBranchStats->upinfer[i] = SCIPgetVarAvgInferences(scip, vars[i], SCIP_BRANCHDIR_UPWARDS);
      varBranchStats->downcutoff[i] = SCIPgetVarAvgCutoffs(scip, vars[i], SCIP_BRANCHDIR_DOWNWARDS);
      varBranchStats->upcutoff[i] = SCIPgetVarAvgCutoffs(scip, vars[i], SCIP_BRANCHDIR_UPWARDS);
   }
}

#ifdef UG_WITH_ZLIB
void
ScipParaDiffSubproblem::write(
      gzstream::ogzstream &out
      )
{

   // std::cout << toString() << std::endl;

   int dummyZero = 0;

#ifdef UG_SCIP_V31_CHECK_POINT_FILES

   out.write((char *)&localInfoIncluded, sizeof(int));
   out.write((char *)&nBoundChanges, sizeof(int));
   for(int i = 0; i < nBoundChanges; i++ )
   {
      out.write((char *)&indicesAmongSolvers[i], sizeof(int));
      out.write((char *)&branchBounds[i], sizeof(SCIP_Real));
      out.write((char *)&boundTypes[i], sizeof(int));
   }

   if( linearConss )
   {
      out.write((char *)&(linearConss->nLinearConss), sizeof(int));
      for(int i = 0; i < linearConss->nLinearConss; i++ )
      {
         out.write((char *)&(linearConss->linearLhss[i]), sizeof(SCIP_Real));
         out.write((char *)&(linearConss->linearRhss[i]), sizeof(SCIP_Real));
         out.write((char *)&(linearConss->nLinearCoefs[i]), sizeof(int));
         for(int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
         {
            out.write((char *)&(linearConss->linearCoefs[i][j]), sizeof(SCIP_Real));
            out.write((char *)&(linearConss->idxLinearCoefsVars[i][j]), sizeof(int));
         }
      }
   }
   else
   {
      out.write((char *)&dummyZero, sizeof(int));
   }

   if( varBranchStats )
   {
      out.write((char *)&(varBranchStats->offset), sizeof(int));
      out.write((char *)&(varBranchStats->nVarBranchStats), sizeof(int));
      for(int i = 0; i < varBranchStats->nVarBranchStats; i++ )
      {
         out.write((char *)&(varBranchStats->idxBranchStatsVars[i]), sizeof(int));
         out.write((char *)&(varBranchStats->downpscost[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->uppscost[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downvsids[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upvsids[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downconflen[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upconflen[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downinfer[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upinfer[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downcutoff[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upcutoff[i]), sizeof(SCIP_Real));
      }
   }
   else
   {
      /* for backward consistency */
      out.write((char *)&dummyZero, sizeof(int));
      out.write((char *)&dummyZero, sizeof(int));
   }

#else


   out.write((char *)&localInfoIncluded, sizeof(int));
   out.write((char *)&nBoundChanges, sizeof(int));
   for(int i = 0; i < nBoundChanges; i++ )
   {
      out.write((char *)&indicesAmongSolvers[i], sizeof(int));
      out.write((char *)&branchBounds[i], sizeof(SCIP_Real));
      out.write((char *)&boundTypes[i], sizeof(int));
   }
   if( linearConss )
   {
      out.write((char *)&(linearConss->nLinearConss), sizeof(int));
      for(int i = 0; i < linearConss->nLinearConss; i++ )
      {
         out.write((char *)&(linearConss->linearLhss[i]), sizeof(SCIP_Real));
         out.write((char *)&(linearConss->linearRhss[i]), sizeof(SCIP_Real));
         out.write((char *)&(linearConss->nLinearCoefs[i]), sizeof(int));
         for(int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
         {
            out.write((char *)&(linearConss->linearCoefs[i][j]), sizeof(SCIP_Real));
            out.write((char *)&(linearConss->idxLinearCoefsVars[i][j]), sizeof(int));
         }
      }
   }
   else
   {
      out.write((char *)&dummyZero, sizeof(int));
   }

   if( boundDisjunctions )
   {
      out.write((char *)&(boundDisjunctions->nBoundDisjunctions), sizeof(int));
      out.write((char *)&(boundDisjunctions->nTotalVarsBoundDisjunctions), sizeof(int));
      for(int i = 0; i < boundDisjunctions->nBoundDisjunctions; i++ )
      {
         out.write((char *)&(boundDisjunctions->nVarsBoundDisjunction[i]), sizeof(int));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionInitial[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionSeparate[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionEnforce[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionCheck[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionPropagate[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionLocal[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionModifiable[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionDynamic[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionRemovable[i]), sizeof(SCIP_Bool));
         out.write((char *)&(boundDisjunctions->flagBoundDisjunctionStickingatnode[i]), sizeof(SCIP_Bool));
         for( int j = 0; j < boundDisjunctions->nVarsBoundDisjunction[i]; j++ )
         {
            out.write((char *)&(boundDisjunctions->idxBoundDisjunctionVars[i][j]), sizeof(int));
            out.write((char *)&(boundDisjunctions->boundTypesBoundDisjunction[i][j]), sizeof(SCIP_BOUNDTYPE));
            out.write((char *)&(boundDisjunctions->boundsBoundDisjunction[i][j]), sizeof(SCIP_Real));
         }
      }
   }
   else
   {
      out.write((char *)&dummyZero, sizeof(int));
   }


   if( varBranchStats )
   {
      out.write((char *)&(varBranchStats->offset), sizeof(int));
      out.write((char *)&(varBranchStats->nVarBranchStats), sizeof(int));
      for(int i = 0; i < varBranchStats->nVarBranchStats; i++ )
      {
         out.write((char *)&(varBranchStats->idxBranchStatsVars[i]), sizeof(int));
         out.write((char *)&(varBranchStats->downpscost[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->uppscost[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downvsids[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upvsids[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downconflen[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upconflen[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downinfer[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upinfer[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->downcutoff[i]), sizeof(SCIP_Real));
         out.write((char *)&(varBranchStats->upcutoff[i]), sizeof(SCIP_Real));
      }
   }
   else
   {
      /* for backward consistency */
      out.write((char *)&dummyZero, sizeof(int));
      out.write((char *)&dummyZero, sizeof(int));
   }


   if( varValues )
   {
      out.write((char *)&(varValues->nVarValueVars), sizeof(int));
      out.write((char *)&(varValues->nVarValues), sizeof(int));
      for(int i = 0; i < varValues->nVarValueVars; i++)
      {
         out.write((char *)&(varValues->idxVarValueVars[i]), sizeof(int));
         out.write((char *)&(varValues->nVarValueValues[i]), sizeof(int));
         if( varValues->nVarValueValues[i] > 0 )
         {
            for(int j = 0; j <  varValues->nVarValueValues[i]; j++ )
            {
               out.write((char *)&(varValues->varValue[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueDownvsids[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varVlaueUpvsids[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueDownconflen[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueUpconflen[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueDowninfer[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueUpinfer[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueDowncutoff[i][j]), sizeof(SCIP_Real));
               out.write((char *)&(varValues->varValueUpcutoff[i][j]), sizeof(SCIP_Real));
            }
         }
      }
   }
   else
   {
      out.write((char *)&dummyZero, sizeof(int));
   }

#endif

#ifdef UG_DEBUG_SOLUTION
   out.write((char *)&includeOptimalSol, sizeof(int));
#endif

}

void
ScipParaDiffSubproblem::read(
      ParaComm *comm,
      gzstream::igzstream &in,
      bool onlyBoundChanges
      )
{

   int dummyInt1 = 0;
   int dummyInt2 = 0;

#ifdef UG_SCIP_V31_CHECK_POINT_FILES

   in.read((char *)&localInfoIncluded, sizeof(int));
   in.read((char *)&nBoundChanges, sizeof(int));
   if( nBoundChanges > 0 )
   {
      indicesAmongSolvers = new int[nBoundChanges];
      branchBounds = new SCIP_Real[nBoundChanges];
      boundTypes = new SCIP_BOUNDTYPE[nBoundChanges];
   }
   for(int i = 0; i < nBoundChanges; i++ )
   {
      in.read((char *)&indicesAmongSolvers[i], sizeof(int));
      in.read((char *)&branchBounds[i], sizeof(SCIP_Real));
      in.read((char *)&boundTypes[i], sizeof(int));
   }
   if( !onlyBoundChanges )
   {
      in.read((char *)&dummyInt1, sizeof(int));
      if( dummyInt1 > 0 )
      {
         linearConss = new ScipParaDiffSubproblemLinearCons();
         linearConss->nLinearConss = dummyInt1;
         linearConss->linearLhss = new SCIP_Real[linearConss->nLinearConss];
         linearConss->linearRhss = new SCIP_Real[linearConss->nLinearConss];
         linearConss->nLinearCoefs = new int[linearConss->nLinearConss];
         linearConss->linearCoefs = new SCIP_Real*[linearConss->nLinearConss];
         linearConss->idxLinearCoefsVars = new int*[linearConss->nLinearConss];
         for(int i = 0; i < linearConss->nLinearConss; i++ )
         {
            in.read((char *)&(linearConss->linearLhss[i]), sizeof(SCIP_Real));
            in.read((char *)&(linearConss->linearRhss[i]), sizeof(SCIP_Real));
            in.read((char *)&(linearConss->nLinearCoefs[i]), sizeof(int));
            assert(linearConss->nLinearCoefs[i] > 0);
            linearConss->linearCoefs[i] = new SCIP_Real[linearConss->nLinearCoefs[i]];
            linearConss->idxLinearCoefsVars[i] = new int[linearConss->nLinearCoefs[i]];
            for(int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
            {
               in.read((char *)&(linearConss->linearCoefs[i][j]), sizeof(SCIP_Real));
               in.read((char *)&(linearConss->idxLinearCoefsVars[i][j]), sizeof(int));
            }
         }
      }

      in.read((char *)&dummyInt1, sizeof(int));
      in.read((char *)&dummyInt2, sizeof(int));
      if( dummyInt2 > 0)
      {
         varBranchStats = new ScipParaDiffSubproblemVarBranchStats();
         varBranchStats->offset = dummyInt1;
         varBranchStats->nVarBranchStats = dummyInt2;
         varBranchStats->idxBranchStatsVars = new int[varBranchStats->nVarBranchStats];
         varBranchStats->downpscost = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->uppscost = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downvsids = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upvsids = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downconflen = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upconflen = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downinfer = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upinfer = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downcutoff = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upcutoff = new SCIP_Real[varBranchStats->nVarBranchStats];
         for(int i = 0; i < varBranchStats->nVarBranchStats; i++ )
         {
            in.read((char *)&(varBranchStats->idxBranchStatsVars[i]), sizeof(int));
            in.read((char *)&(varBranchStats->downpscost[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->uppscost[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downvsids[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upvsids[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downconflen[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upconflen[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downinfer[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upinfer[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downcutoff[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upcutoff[i]), sizeof(SCIP_Real));
         }
      }

   }
   else
   {
      assert( linearConss == 0);
      SCIP_Real dummyReal;
      int       dummyInt;
      int       nConss;
      in.read((char *)&nConss, sizeof(int));
      if( nConss > 0 )
      {
         for(int i = 0; i < nConss; i++ )
         {
            int nCoefs;
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&nCoefs, sizeof(int));
            assert(nCoefs > 0);
            for(int j = 0; j < nCoefs; j++ )
            {
               in.read((char *)&dummyReal, sizeof(SCIP_Real));
               in.read((char *)&dummyInt, sizeof(int));
            }
         }
      }
      assert( varBranchStats == 0 );
      int nStats;
      in.read((char *)&dummyInt, sizeof(int));
      in.read((char *)&nStats, sizeof(int));

      for(int i = 0; i < nStats; i++ )
      {
         in.read((char *)&dummyInt, sizeof(int));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
         in.read((char *)&dummyReal, sizeof(SCIP_Real));
      }
   }

#else

   in.read((char *)&localInfoIncluded, sizeof(int));
   in.read((char *)&nBoundChanges, sizeof(int));
   if( nBoundChanges > 0 )
   {
      indicesAmongSolvers = new int[nBoundChanges];
      branchBounds = new SCIP_Real[nBoundChanges];
      boundTypes = new SCIP_BOUNDTYPE[nBoundChanges];
   }
   for(int i = 0; i < nBoundChanges; i++ )
   {
      in.read((char *)&indicesAmongSolvers[i], sizeof(int));
      in.read((char *)&branchBounds[i], sizeof(SCIP_Real));
      in.read((char *)&boundTypes[i], sizeof(int));
   }
   if( !onlyBoundChanges )
   {

      in.read((char *)&dummyInt1, sizeof(int));
      if( dummyInt1 > 0 )
      {
         linearConss = new ScipParaDiffSubproblemLinearCons();
         linearConss->nLinearConss = dummyInt1;
         linearConss->linearLhss = new SCIP_Real[linearConss->nLinearConss];
         linearConss->linearRhss = new SCIP_Real[linearConss->nLinearConss];
         linearConss->nLinearCoefs = new int[linearConss->nLinearConss];
         linearConss->linearCoefs = new SCIP_Real*[linearConss->nLinearConss];
         linearConss->idxLinearCoefsVars = new int*[linearConss->nLinearConss];
         for(int i = 0; i < linearConss->nLinearConss; i++ )
         {
            in.read((char *)&(linearConss->linearLhss[i]), sizeof(SCIP_Real));
            in.read((char *)&(linearConss->linearRhss[i]), sizeof(SCIP_Real));
            in.read((char *)&(linearConss->nLinearCoefs[i]), sizeof(int));
            assert(linearConss->nLinearCoefs[i] > 0);
            linearConss->linearCoefs[i] = new SCIP_Real[linearConss->nLinearCoefs[i]];
            linearConss->idxLinearCoefsVars[i] = new int[linearConss->nLinearCoefs[i]];
            for(int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
            {
               in.read((char *)&(linearConss->linearCoefs[i][j]), sizeof(SCIP_Real));
               in.read((char *)&(linearConss->idxLinearCoefsVars[i][j]), sizeof(int));
            }
         }
      }

      in.read((char *)&dummyInt1, sizeof(int));
      if( dummyInt1 > 0 )
      {
         boundDisjunctions = new ScipParaDiffSubproblemBoundDisjunctions();
         boundDisjunctions->nBoundDisjunctions = dummyInt1;
         in.read((char *)&(boundDisjunctions->nTotalVarsBoundDisjunctions), sizeof(int));
         boundDisjunctions->nVarsBoundDisjunction = new int[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionInitial = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionSeparate = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionEnforce = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionCheck = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionPropagate = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionLocal = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionModifiable = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionDynamic = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionRemovable = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->flagBoundDisjunctionStickingatnode = new SCIP_Bool[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->idxBoundDisjunctionVars = new int*[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->boundTypesBoundDisjunction = new SCIP_BOUNDTYPE*[boundDisjunctions->nBoundDisjunctions];
         boundDisjunctions->boundsBoundDisjunction = new SCIP_Real*[boundDisjunctions->nBoundDisjunctions];
         for(int i = 0; i < boundDisjunctions->nBoundDisjunctions; i++ )
         {
            in.read((char *)&(boundDisjunctions->nVarsBoundDisjunction[i]), sizeof(int));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionInitial[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionSeparate[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionEnforce[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionCheck[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionPropagate[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionLocal[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionModifiable[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionDynamic[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionRemovable[i]), sizeof(SCIP_Bool));
            in.read((char *)&(boundDisjunctions->flagBoundDisjunctionStickingatnode[i]), sizeof(SCIP_Bool));
            if( boundDisjunctions->nVarsBoundDisjunction[i] > 0 )
            {
               boundDisjunctions->idxBoundDisjunctionVars[i] = new int[boundDisjunctions->nVarsBoundDisjunction[i]];
               boundDisjunctions->boundTypesBoundDisjunction[i] = new SCIP_BOUNDTYPE[boundDisjunctions->nVarsBoundDisjunction[i]];
               boundDisjunctions->boundsBoundDisjunction[i] = new SCIP_Real[boundDisjunctions->nVarsBoundDisjunction[i]];
               for( int j = 0; j < boundDisjunctions->nVarsBoundDisjunction[i]; j++ )
               {
                  in.read((char *)&(boundDisjunctions->idxBoundDisjunctionVars[i][j]), sizeof(int));
                  in.read((char *)&(boundDisjunctions->boundTypesBoundDisjunction[i][j]), sizeof(SCIP_BOUNDTYPE));
                  in.read((char *)&(boundDisjunctions->boundsBoundDisjunction[i][j]), sizeof(SCIP_Real));
               }
            }
         }
      }


      in.read((char *)&dummyInt1, sizeof(int));
      in.read((char *)&dummyInt2, sizeof(int));
      if( dummyInt2 > 0)
      {
         varBranchStats = new ScipParaDiffSubproblemVarBranchStats();
         varBranchStats->offset = dummyInt1;
         varBranchStats->nVarBranchStats = dummyInt2;
         varBranchStats->idxBranchStatsVars = new int[varBranchStats->nVarBranchStats];
         varBranchStats->downpscost = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->uppscost = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downvsids = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upvsids = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downconflen = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upconflen = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downinfer = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upinfer = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->downcutoff = new SCIP_Real[varBranchStats->nVarBranchStats];
         varBranchStats->upcutoff = new SCIP_Real[varBranchStats->nVarBranchStats];
         for(int i = 0; i < varBranchStats->nVarBranchStats; i++ )
         {
            in.read((char *)&(varBranchStats->idxBranchStatsVars[i]), sizeof(int));
            in.read((char *)&(varBranchStats->downpscost[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->uppscost[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downvsids[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upvsids[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downconflen[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upconflen[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downinfer[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upinfer[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->downcutoff[i]), sizeof(SCIP_Real));
            in.read((char *)&(varBranchStats->upcutoff[i]), sizeof(SCIP_Real));
         }
      }

      in.read((char *)&dummyInt1, sizeof(int));
      if( dummyInt1 > 0 )
      {
         varValues = new ScipParaDiffSubproblemVarValues();
         varValues->nVarValueVars = dummyInt1;
         in.read((char *)&(varValues->nVarValues), sizeof(int));
         varValues->idxVarValueVars     = new int[varValues->nVarValueVars];
         varValues->nVarValueValues     = new int[varValues->nVarValueVars];
         varValues->varValue            = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueDownvsids   = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varVlaueUpvsids     = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueDownconflen = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueUpconflen   = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueDowninfer   = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueUpinfer     = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueDowncutoff  = new SCIP_Real*[varValues->nVarValueVars];
         varValues->varValueUpcutoff    = new SCIP_Real*[varValues->nVarValueVars];
         for(int i = 0; i < varValues->nVarValueVars; i++)
         {
            in.read((char *)&varValues->idxVarValueVars[i], sizeof(int));
            in.read((char *)&varValues->nVarValueValues[i], sizeof(int));
            if( varValues->nVarValueValues[i] > 0 )
            {
               varValues->varValue[i]            = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueDownvsids[i]   = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varVlaueUpvsids[i]     = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueDownconflen[i] = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueUpconflen[i]   = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueDowninfer[i]   = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueUpinfer[i]     = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueDowncutoff[i]  = new SCIP_Real[varValues->nVarValueValues[i]];
               varValues->varValueUpcutoff[i]    = new SCIP_Real[varValues->nVarValueValues[i]];
               for(int j = 0; j <  varValues->nVarValueValues[i]; j++ )
               {
                  in.read((char *)&(varValues->varValue[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueDownvsids[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varVlaueUpvsids[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueDownconflen[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueUpconflen[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueDowninfer[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueUpinfer[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueDowncutoff[i][j]), sizeof(SCIP_Real));
                  in.read((char *)&(varValues->varValueUpcutoff[i][j]), sizeof(SCIP_Real));
               }
            }
         }
      }
   }
   else
   {
      assert( linearConss == 0);
      SCIP_Real dummyReal;
      int       dummyInt;
      int       nConss;
      in.read((char *)&nConss, sizeof(int));
      if( nConss > 0 )
      {
         for(int i = 0; i < nConss; i++ )
         {
            int nCoefs;
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&nCoefs, sizeof(int));
            assert(nCoefs > 0);
            for(int j = 0; j < nCoefs; j++ )
            {
               in.read((char *)&dummyReal, sizeof(SCIP_Real));
               in.read((char *)&dummyInt, sizeof(int));
            }
         }
      }
      int nBTemp = 0;
      int bInt = 0;
      SCIP_Bool bBool = 0;
      SCIP_Real bReal = 0.0;
      SCIP_BOUNDTYPE bType = SCIP_BOUNDTYPE_LOWER;
      in.read((char *)&nBTemp, sizeof(int));
      if( nBTemp > 0 )
      {
         in.read((char *)&bInt, sizeof(int));
         for(int i = 0; i < nBTemp; i++ )
         {
            int nBtemp2 = 0;
            in.read((char *)&nBtemp2, sizeof(int));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            in.read((char *)&bBool, sizeof(SCIP_Bool));
            if( nBtemp2 > 0 )
            {
               for( int j = 0; j < nBtemp2; j++ )
               {
                  in.read((char *)&bInt, sizeof(int));
                  in.read((char *)&bType, sizeof(SCIP_BOUNDTYPE));
                  in.read((char *)&bReal, sizeof(SCIP_Real));
               }
            }
         }
      }


      assert( varBranchStats == 0 );
      int nStats;
      in.read((char *)&dummyInt, sizeof(int));
      in.read((char *)&nStats, sizeof(int));

      if( nStats > 0 )
      {
         for(int i = 0; i < nStats; i++ )
         {
            in.read((char *)&dummyInt, sizeof(int));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
            in.read((char *)&dummyReal, sizeof(SCIP_Real));
         }
      }
      int nTemp1 = 0;
      in.read((char *)&nTemp1, sizeof(int));
      if( nTemp1 > 0 )
      {
         in.read((char *)&dummyInt, sizeof(int));
         for(int i = 0; i < nTemp1; i++)
         {
            int nTemp2 = 0;
            in.read((char *)&dummyInt, sizeof(int));
            in.read((char *)&nTemp2, sizeof(int));
            if( nTemp2 > 0 )
            {
               for(int j = 0; j <  nTemp2; j++ )
               {
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
                  in.read((char *)&dummyReal, sizeof(SCIP_Real));
               }
            }
         }
      }
   }
#endif

#ifdef UG_DEBUG_SOLUTION
   in.read((char *)&includeOptimalSol, sizeof(int));
#endif
}
#endif // End of UG_WITH_ZLIB

/** get fixed variables **/
int
ScipParaDiffSubproblem::getFixedVariables(
      ParaInstance *instance,
      ParaFixedVariable **fixedVars
      )
{
   ScipParaInstance *scipInstance = dynamic_cast< ScipParaInstance* >(instance);
   *fixedVars = new ParaFixedVariable[nBoundChanges];   //  allocate space for the maximum possible numbers
   int n = 0;
   int k = 0;
   for( int i = 0; i < nBoundChanges; i++ )
   {
      int probindex = indicesAmongSolvers[i];
      if( scipInstance->isOriginalIndeciesMap() )
      {
         probindex = scipInstance->getOrigProbIndex(indicesAmongSolvers[i]);
      }
      /* skip inactive varibales */
      if( probindex < 0 ) continue;

      switch( static_cast<SCIP_VARTYPE>(scipInstance->getVarType( probindex ) ) )
      {
      case SCIP_VARTYPE_BINARY:
         if( boundTypes[i] == SCIP_BOUNDTYPE_LOWER )
         {
            assert( EPSEQ(branchBounds[i], scipInstance->getVarUb(probindex), DEFAULT_NUM_EPSILON ) );
         }
         else
         {
            assert( EPSEQ(branchBounds[i], scipInstance->getVarLb(probindex), DEFAULT_NUM_EPSILON ) );
         }
         for( k = 0 ; k < n; k++ )
         {
            if( indicesAmongSolvers[i] == (*fixedVars)[k].index )   // when I checked, this case happened!
               break;
         }
         if( k != n ) break;
         (*fixedVars)[n].nSameValue = 0;
         (*fixedVars)[n].index = indicesAmongSolvers[i];
         (*fixedVars)[n].value = branchBounds[i];
         (*fixedVars)[n].mnode = 0;
         (*fixedVars)[n].next = 0;
         (*fixedVars)[n].prev = 0;
         n++;
         break;
      case SCIP_VARTYPE_INTEGER:
      case SCIP_VARTYPE_IMPLINT:
      case SCIP_VARTYPE_CONTINUOUS:
         if( boundTypes[i] == SCIP_BOUNDTYPE_LOWER )
         {
            if( !EPSEQ(branchBounds[i], scipInstance->getVarUb(probindex), DEFAULT_NUM_EPSILON ) )
            {
               int j = i + 1;
               for( ; j < nBoundChanges; j++ )
               {
                  if( indicesAmongSolvers[i] == indicesAmongSolvers[j] &&
                        boundTypes[j] == SCIP_BOUNDTYPE_UPPER &&
                        EPSEQ( branchBounds[i], branchBounds[j], DEFAULT_NUM_EPSILON )
                        )
                  {
                     break;
                  }
               }
               if( j >= nBoundChanges ) break;
            }
         }
         else
         {
            if( !EPSEQ(branchBounds[i], scipInstance->getVarLb(probindex), DEFAULT_NUM_EPSILON ) )
            {
               int j = i + 1;
               for( ; j < nBoundChanges; j++ )
               {
                  if( indicesAmongSolvers[i] == indicesAmongSolvers[j] &&
                        boundTypes[j] == SCIP_BOUNDTYPE_LOWER &&
                        EPSEQ( branchBounds[i], branchBounds[j], DEFAULT_NUM_EPSILON )
                        )
                  {
                     break;
                  }
               }
               if( j >= nBoundChanges ) break;
            }
         }
         for(k = 0; k < n; k++ )
         {
            if( indicesAmongSolvers[i] == (*fixedVars)[k].index )   // when I checked, this case happened!
               break;
         }
         if( k != n ) break;
         (*fixedVars)[n].nSameValue = 0;
         (*fixedVars)[n].index = indicesAmongSolvers[i];
         (*fixedVars)[n].value = branchBounds[i];
         (*fixedVars)[n].mnode = 0;
         (*fixedVars)[n].next = 0;
         (*fixedVars)[n].prev = 0;
         n++;

         break;
      default:
         THROW_LOGICAL_ERROR2("Invalid Variable Type = ", static_cast<int>(scipInstance->getVarType(probindex) ) );
      }
   }
   if( n == 0 )
   {
      delete [] *fixedVars;
      *fixedVars = 0;
   }
   return n;
}

/** create new ParaDiffSubproblem using fixed variables information */
ParaDiffSubproblem*
ScipParaDiffSubproblem::createDiffSubproblem(
      ParaComm          *comm,
	   ParaInitiator     *initiator,
      int                n,
      ParaFixedVariable *fixedVars
      )
{
   ScipParaDiffSubproblem *diffSubproblem = dynamic_cast<ScipParaDiffSubproblem*>( comm->createParaDiffSubproblem() );
   int nNewBranches = 0;
   diffSubproblem->indicesAmongSolvers = new int[nBoundChanges];
   diffSubproblem->branchBounds = new SCIP_Real[nBoundChanges];
   diffSubproblem->boundTypes = new SCIP_BOUNDTYPE[nBoundChanges];
   
   ScipParaInitiator *scipParaInitiator = dynamic_cast<ScipParaInitiator*>(initiator);
   
   if( scipParaInitiator->areTightenedVarBounds() )
   {
      for( int i = 0; i < nBoundChanges; i++ )
      {
         bool updated = false;
         for( int j = 0; j < n; j++ )
         {
            if( indicesAmongSolvers[i] == fixedVars[j].index )
            {
               diffSubproblem->indicesAmongSolvers[nNewBranches] = indicesAmongSolvers[i];
               diffSubproblem->branchBounds[nNewBranches] = branchBounds[i];
               diffSubproblem->boundTypes[nNewBranches] = boundTypes[i];
               nNewBranches++;
               updated = true;
               break;
            }
         }
         // tightened local bound changes including global bound changes must be received already
         if( !updated )
         {
            if( boundTypes[i] == SCIP_BOUNDTYPE_LOWER &&
                  EPSGT( scipParaInitiator->getTightenedVarLbs(indicesAmongSolvers[i]), branchBounds[i], MINEPSILON )
                  )
            {
               diffSubproblem->indicesAmongSolvers[nNewBranches] = indicesAmongSolvers[i];
               diffSubproblem->branchBounds[nNewBranches] = scipParaInitiator->getTightenedVarLbs(indicesAmongSolvers[i]);
               diffSubproblem->boundTypes[nNewBranches] = boundTypes[i];
               nNewBranches++;
            }
            if( boundTypes[i] == SCIP_BOUNDTYPE_UPPER &&
                  EPSLT( scipParaInitiator->getTightenedVarUbs(indicesAmongSolvers[i]), branchBounds[i], MINEPSILON )
                  )
            {
               diffSubproblem->indicesAmongSolvers[nNewBranches] = indicesAmongSolvers[i];
               diffSubproblem->branchBounds[nNewBranches] = scipParaInitiator->getTightenedVarUbs(indicesAmongSolvers[i]);
               diffSubproblem->boundTypes[nNewBranches] = boundTypes[i];
               nNewBranches++;
            }
         }
      }
   }
   else
   {
      for( int i = 0; i < nBoundChanges; i++ )
      {
         for( int j = 0; j < n; j++ )
         {
            if( indicesAmongSolvers[i] == fixedVars[j].index )
            {
               diffSubproblem->indicesAmongSolvers[nNewBranches] = indicesAmongSolvers[i];
               diffSubproblem->branchBounds[nNewBranches] = branchBounds[i];
               diffSubproblem->boundTypes[nNewBranches] = boundTypes[i];
               nNewBranches++;
               break;
            }
         }
      }
   }
   diffSubproblem->nBoundChanges = nNewBranches;
#ifdef UG_DEBUG_SOLUTION
   diffSubproblem->includeOptimalSol = includeOptimalSol;
#endif
   return diffSubproblem;
}

/** stringfy ParaCalculationState */
const std::string
ScipParaDiffSubproblem::toString(
      )
{
   std::ostringstream s;

   s << "localInfoIncluded = " << localInfoIncluded << std::endl;
   s << "nBranches = " <<  nBoundChanges << std::endl;
   for(int i = 0; i < nBoundChanges; i++ )
   {
      s << "indicesAmongSolvers[" << i << "] = " << indicesAmongSolvers[i] << std::endl;
      s << "branchBounds[" << i << "] = " << branchBounds[i] << std::endl;
      s << "boudTypes[" << i << "] = " << static_cast<int>(boundTypes[i]) << std::endl;
   }

   if( linearConss )
   {
      s << "nLinearConss = " << linearConss->nLinearConss << std::endl;
      for(int i = 0; i < linearConss->nLinearConss; i++ )
      {
         s << "linearLhss[" << i << "] = " << linearConss->linearLhss[i] << std::endl;
         s << "linearRhss[" << i << "] = " << linearConss->linearRhss[i] << std::endl;
         s << "nLinearCoefs[" << i << "] = " << linearConss->nLinearCoefs[i] << std::endl;
         for( int j = 0; j < linearConss->nLinearCoefs[i]; j++ )
         {
            s << "linearCoefs[" << i << "][" << j << "] = " << linearConss->linearCoefs[i][j] << std::endl;
            s << "idxLinearCoefsVars[" << i << "][" << j << "] = " << linearConss->idxLinearCoefsVars[i][j] << std::endl;
         }
      }
   }

   if( boundDisjunctions )
   {
      s << "nBoundDisjunctions = " << boundDisjunctions->nBoundDisjunctions << std::endl;
      s << "nTotalVarsBoundDisjunctions = " << boundDisjunctions->nTotalVarsBoundDisjunctions << std::endl;
      for(int i = 0; i < boundDisjunctions->nBoundDisjunctions; i++ )
      {
         s << "nVarsBoundDisjunction[" << i << "] = " <<  boundDisjunctions->nVarsBoundDisjunction[i] << std::endl;
         s << "flagBoundDisjunctionInitial[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionInitial[i] << std::endl;
         s << "flagBoundDisjunctionSeparate[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionSeparate[i] << std::endl;
         s << "flagBoundDisjunctionEnforce[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionEnforce[i] << std::endl;
         s << "flagBoundDisjunctionCheck[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionCheck[i] << std::endl;
         s << "flagBoundDisjunctionPropagate[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionPropagate[i] << std::endl;
         s << "flagBoundDisjunctionLocal[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionLocal[i] << std::endl;
         s << "flagBoundDisjunctionModifiable[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionModifiable[i] << std::endl;
         s << "flagBoundDisjunctionDynamic[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionDynamic[i] << std::endl;
         s << "flagBoundDisjunctionRemovable[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionRemovable[i] << std::endl;
         s << "flagBoundDisjunctionStickingatnode[" << i << "] = " << boundDisjunctions->flagBoundDisjunctionStickingatnode[i] << std::endl;
         for(int j = 0; j < boundDisjunctions->nVarsBoundDisjunction[i]; j++ )
         {
            s << "idxBoundDisjunctionVars[" << i << "][" << j << "] = " << boundDisjunctions->idxBoundDisjunctionVars[i][j] << std::endl;
            s << "boundTypesBoundDisjunction[" << i << "][" << j << "] = " << static_cast<int>(boundDisjunctions->boundTypesBoundDisjunction[i][j]) << std::endl;
            s << "boundsBoundDisjunction[" << i << "][" << j << "] = " << boundDisjunctions->boundsBoundDisjunction[i][j] << std::endl;
         }
      }
   }

   if( varBranchStats )
   {
      s << "offset = " << varBranchStats->offset << std::endl;
      s << "nVarBranchStats = " << varBranchStats->nVarBranchStats << std::endl;
      for(int i = 0; i < varBranchStats->nVarBranchStats; i++ )
      {
         s << "idxLBranchStatsVars[" << i << "] = " << varBranchStats->idxBranchStatsVars[i] << std::endl;
         s << "downpscost[" << i << "] = " << varBranchStats->downpscost[i] << std::endl;
         s << "uppscost[" << i << "] = " << varBranchStats->uppscost[i] << std::endl;
         s << "downvsids[" << i << "] = " << varBranchStats->downvsids[i] << std::endl;
         s << "upvsids[" << i << "] = " << varBranchStats->upvsids[i] << std::endl;
         s << "downconflen[" << i << "] = " << varBranchStats->downconflen[i] << std::endl;
         s << "upconflen[" << i << "] = " << varBranchStats->upconflen[i] << std::endl;
         s << "downinfer[" << i << "] = " << varBranchStats->downinfer[i] << std::endl;
         s << "upinfer[" << i << "] = " << varBranchStats->upinfer[i] << std::endl;
         s << "downcutoff[" << i << "] = " << varBranchStats->downcutoff[i] << std::endl;
         s << "upcutoff[" << i << "] = " << varBranchStats->upcutoff[i] << std::endl;
      }
   }

   if( varValues )
   {
      s << "nVarValueVars = " << varValues->nVarValueVars << std::endl;
      for(int i = 0; i < varValues->nVarValueVars; i++ )
      {
         s << "idxVarValueVars[" << i << "] = " << varValues->idxVarValueVars[i] << std::endl;
         s << "nVarValueValues[" << i << "] = " << varValues->nVarValueValues[i] << std::endl;
         if( varValues->nVarValueValues[i] > 0 )
         {
            for( int j = 0; j < varValues->nVarValueValues[i]; j++ )
            {
               s << "varValue[" << i << "][" << j << "] = " << varValues->varValue[i][j] << std::endl;
               s << "varValueDownvsids[" << i << "][" << j << "] = " << varValues->varValueDownvsids[i][j] << std::endl;
               s << "varVlaueUpvsids[" << i << "][" << j << "] = " << varValues->varVlaueUpvsids[i][j] << std::endl;
               s << "varValueDownconflen[" << i << "][" << j << "] = " << varValues->varValueDownconflen[i][j] << std::endl;
               s << "varValueUpconflen[" << i << "][" << j << "] = " << varValues->varValueUpconflen[i][j] << std::endl;
               s << "varValueDowninfer[" << i << "][" << j << "] = " << varValues->varValueDowninfer[i][j] << std::endl;
               s << "varValueUpinfer[" << i << "][" << j << "] = " << varValues->varValueUpinfer[i][j] << std::endl;
               s << "varValueDowncutoff[" << i << "][" << j << "] = " << varValues->varValueDowncutoff[i][j] << std::endl;
               s << "varValueUpcutoff[" << i << "][" << j << "] = " << varValues->varValueUpcutoff[i][j] << std::endl;
            }
         }
      }

   }
   return s.str();
}


