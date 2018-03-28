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

/**@file    scipDiffParamSetMpi.cpp
 * @brief   ScipDiffParamSet extension for MPI communication.
 * @author  Yuji Shinano
 *
 *
 *
 */

/*---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0----+----1----+----2*/


#include <string.h>
#include <cassert>
#include "scip/scip.h"
#include "ug/paraCommMpi.h"
#include "scipDiffParamSetMpi.h"

using namespace UG;
using namespace ParaSCIP;

/** create scipDiffParamSetPreType */
MPI_Datatype
ScipDiffParamSetMpi::createDatatype1(
      )
{
   MPI_Datatype datatype;

   int blockLengthsPre[13];
   MPI_Aint displacementsPre[13];
   MPI_Datatype typesPre[13];

   MPI_Aint startAddress = 0;
   MPI_Aint address = 0;

   for( int i = 0; i < 13; i++ ){
       blockLengthsPre[i] = 1;
       typesPre[i] = MPI_INT;
   }

   MPI_CALL(
      MPI_Get_address( &numBoolParams, &startAddress )
   );
   displacementsPre[0] = 0;
   MPI_CALL(
      MPI_Get_address( &boolParamNamesSize, &address )
   );
   displacementsPre[1] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &numIntParams, &address )
   );
   displacementsPre[2] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &intParamNamesSize, &address )
   );
   displacementsPre[3] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &numLongintParams, &address )
   );
   displacementsPre[4] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &longintParamNamesSize, &address )
   );
   displacementsPre[5] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &numRealParams, &address )
   );
   displacementsPre[6] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &realParamNamesSize, &address )
   );
   displacementsPre[7] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &numCharParams, &address )
   );
   displacementsPre[8] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &charParamNamesSize, &address )
   );
   displacementsPre[9] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &numStringParams, &address )
   );
   displacementsPre[10] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &stringParamNamesSize, &address )
   );
   displacementsPre[11] = address - startAddress;
   MPI_CALL(
      MPI_Get_address( &stringParamValuesSize, &address )
   );
   displacementsPre[12] = address - startAddress;

   MPI_CALL(
         MPI_Type_create_struct(13, blockLengthsPre, displacementsPre, typesPre, &datatype)
         );

   return datatype;

}

/** create scipDiffParamSetType */
MPI_Datatype
ScipDiffParamSetMpi::createDatatype2(
      bool memAllocNecessary
      )
{
   MPI_Datatype datatype;

   int blockLengths[12];
   MPI_Aint displacements[12];
   MPI_Datatype types[12];

   MPI_Aint startAddress = 0;
   MPI_Aint address = 0;

   if( memAllocNecessary ){
      allocateMemoty();
   }

   MPI_CALL(
      MPI_Get_address( boolParamNames, &startAddress )
   );
   blockLengths[0] = boolParamNamesSize;
   displacements[0] = 0;
   types[0] = MPI_CHAR;

   MPI_CALL(
      MPI_Get_address( boolParamValues, &address )
   );
   blockLengths[1] = numBoolParams;
   displacements[1] = address - startAddress;
   types[1] = MPI_UNSIGNED;

   MPI_CALL(
      MPI_Get_address( intParamNames, &address )
   );
   blockLengths[2] = intParamNamesSize;
   displacements[2] = address - startAddress;
   types[2] = MPI_CHAR;

   MPI_CALL(
      MPI_Get_address( intParamValues, &address )
   );
   blockLengths[3] = numIntParams;
   displacements[3] = address - startAddress;
   types[3] = MPI_INT;
   MPI_CALL(
      MPI_Get_address( longintParamNames, &address )
   );
   blockLengths[4] = longintParamNamesSize;
   displacements[4] = address - startAddress;
   types[4] = MPI_CHAR;
   MPI_CALL(
      MPI_Get_address( longintParamValues, &address )
   );
   blockLengths[5] = numLongintParams;
   displacements[5] = address - startAddress;
#ifdef _ALIBABA
   types[5] = MPI_LONG;
#else
   types[5] = MPI_LONG_LONG;
#endif
   MPI_CALL(
      MPI_Get_address( realParamNames, &address )
   );
   blockLengths[6] = realParamNamesSize;
   displacements[6] = address - startAddress;
   types[6] = MPI_CHAR;
   MPI_CALL(
      MPI_Get_address( realParamValues, &address )
   );
   blockLengths[7] = numRealParams;
   displacements[7] = address - startAddress;
   types[7] = MPI_DOUBLE;
   MPI_CALL(
      MPI_Get_address( charParamNames, &address )
   );
   blockLengths[8] = charParamNamesSize;
   displacements[8] = address - startAddress;
   types[8] = MPI_CHAR;
   MPI_CALL(
      MPI_Get_address( charParamValues, &address )
   );
   blockLengths[9] = numCharParams;
   displacements[9] = address - startAddress;
   types[9] = MPI_CHAR;
   MPI_CALL(
      MPI_Get_address( stringParamNames, &address )
   );
   blockLengths[10] = stringParamNamesSize;
   displacements[10] = address - startAddress;
   types[10] = MPI_CHAR;
   MPI_CALL(
      MPI_Get_address( stringParamValues, &address )
   );
   blockLengths[11] = stringParamValuesSize;
   displacements[11] = address - startAddress;
   types[11] = MPI_CHAR;

   MPI_CALL(
         MPI_Type_create_struct(12, blockLengths, displacements, types, &datatype)
         );

   return datatype;
}

/** send solution data to the rank */
int
ScipDiffParamSetMpi::bcast(
      ParaComm *comm,
      int root
      )
{
   DEF_PARA_COMM( commMpi, comm);

   MPI_Datatype datatype = createDatatype1();
   MPI_CALL(
      MPI_Type_commit( &datatype )
   );
   PARA_COMM_CALL(
      commMpi->ubcast(&numBoolParams, 1, datatype, root)
   );
   MPI_CALL(
      MPI_Type_free( &datatype )
   );

   if( comm->getRank() == root )
   {
      datatype = createDatatype2(false);
   }
   else
   {
      datatype = createDatatype2(true);
   }
   MPI_CALL(
      MPI_Type_commit( &datatype )
   );
   PARA_COMM_CALL(
      commMpi->ubcast(boolParamNames, 1, datatype, root)
   );
   MPI_CALL(
      MPI_Type_free( &datatype )
   );
   return 0;
}

/** send solution data to the rank */
int
ScipDiffParamSetMpi::send(
      ParaComm *comm,
      int dest
      )
{
   DEF_PARA_COMM( commMpi, comm);
   MPI_Datatype datatype = createDatatype1();
   MPI_CALL(
      MPI_Type_commit( &datatype )
   );
   PARA_COMM_CALL(
      commMpi->usend(&numBoolParams, 1, datatype, dest, TagSolverDiffParamSet1)
   );
   MPI_CALL(
      MPI_Type_free( &datatype )
   );

   datatype = createDatatype2(false);
   MPI_CALL(
      MPI_Type_commit( &datatype )
   );
   PARA_COMM_CALL(
      commMpi->usend(boolParamNames, 1, datatype, dest, TagSolverDiffParamSet2)
   );
   MPI_CALL(
      MPI_Type_free( &datatype )
   );
   return 0;
}

 /** receive solution data from the source rank */
int
ScipDiffParamSetMpi::receive(
       ParaComm *comm,
       int source
       )
{
   DEF_PARA_COMM( commMpi, comm);
   MPI_Datatype datatype = createDatatype1();
   MPI_CALL(
      MPI_Type_commit( &datatype )
   );
   PARA_COMM_CALL(
      commMpi->ureceive(&numBoolParams, 1, datatype, source, TagSolverDiffParamSet1)
   );
   MPI_CALL(
      MPI_Type_free( &datatype )
   );

   datatype = createDatatype2(true);
   MPI_CALL(
      MPI_Type_commit( &datatype )
   );
   PARA_COMM_CALL(
       commMpi->ureceive(boolParamNames, 1, datatype, source, TagSolverDiffParamSet2)
   );
   MPI_CALL(
      MPI_Type_free( &datatype )
   );
   return 0;
}
