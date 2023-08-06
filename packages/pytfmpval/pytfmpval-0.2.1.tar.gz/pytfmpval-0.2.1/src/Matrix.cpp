/*
 *  Matrix.cpp
 *  pvalue
 *
 *  Created by Jean-Stéphane Varré on 02/07/07.
 *  Copyright 2007 LIFL-USTL-INRIA. All rights reserved.
 *
 */

#include "Matrix.h"


#define MEMORYCOUNT

void Matrix::computesIntegerMatrix (double granularity, bool sortColumns) {
  double minS = 0, maxS = 0;
  double scoreRange;
  
  // computes precision
  for (int i = 0; i < length; i++) {
    double min = mat[0][i];
    double max = min;
    for (int k = 1; k < 4; k++ )  {
      min = ((min < mat[k][i])?min:(mat[k][i]));
      max = ((max > mat[k][i])?max:(mat[k][i]));
    }
    minS += min;
    maxS += max;
  } 
  
  // score range
  scoreRange = maxS - minS + 1;
  
  if (granularity > 1.0) {
    this->granularity = granularity / scoreRange;
  } else if (granularity < 1.0) {
    this->granularity = 1.0 / granularity;
  } else {
    this->granularity = 1.0;
  }
  
  matInt = new long long *[length];
  for (int k = 0; k < 4; k++ ) {
    matInt[k] = new long long[length];
    for (int p = 0 ; p < length; p++) {
      matInt[k][p] = ROUND_TO_INT((double)(mat[k][p]*this->granularity)); 
    }
  }
  
  this->errorMax = 0.0;
  for (int i = 1; i < length; i++) {
    double maxE = mat[0][i] * this->granularity - (matInt[0][i]);
    for (int k = 1; k < 4; k++) {
      maxE = ((maxE < mat[k][i] * this->granularity - matInt[k][i])?(mat[k][i] * this->granularity - (matInt[k][i])):(maxE));
    }
    this->errorMax += maxE;
  }
  
  if (sortColumns) {
    // sort the columns : the first column is the one with the greatest value
    long long min = 0;
    for (int i = 0; i < length; i++) {
      for (int k = 0; k < 4; k++) {
        min = MIN(min,matInt[k][i]);
      }
    }
    min --;
    long long *maxs = new long long [length];
    for (int i = 0; i < length; i++) {
      maxs[i] = matInt[0][i];
      for (int k = 1; k < 4; k++) {
        if (maxs[i] < matInt[k][i]) {
          maxs[i] = matInt[k][i];
        }
      }
    }
    long long **mattemp = new long long *[4];
    for (int k = 0; k < 4; k++) {        
      mattemp[k] = new long long [length];
    }
    for (int i = 0; i < length; i++) {
      long long max = maxs[0];
      int p = 0;
      for (int j = 1; j < length; j++) {
        if (max < maxs[j]) {
          max = maxs[j];
          p = j;
        }
      }
      maxs[p] = min;
      for (int k = 0; k < 4; k++) {        
        mattemp[k][i] = matInt[k][p];
      }
    }
    
    for (int k = 0; k < 4; k++)  {
      for (int i = 0; i < length; i++) {
        matInt[k][i] = mattemp[k][i];
      }
    }

    for (int k = 0; k < 4; k++) {        
      delete[] mattemp[k];
    }
    delete[] mattemp;
    delete[] maxs;
  }
  
  // computes offsets
  this->offset = 0;
  offsets = new long long [length];
  for (int i = 0; i < length; i++) {
    long long min = matInt[0][i];
    for (int k = 1; k < 4; k++ )  {
      min = ((min < matInt[k][i])?min:(matInt[k][i]));
    }
    offsets[i] = -min;
    for (int k = 0; k < 4; k++ )  {
      matInt[k][i] += offsets[i];  
    }
    this->offset += offsets[i];
  }
  
  // look for the minimum score of the matrix for each column
  minScoreColumn = new long long [length];
  maxScoreColumn = new long long [length];
  //sum            = new long long [length];
  minScore = 0;
  maxScore = 0;
  for (int i = 0; i < length; i++) {
    minScoreColumn[i] = matInt[0][i];
    maxScoreColumn[i] = matInt[0][i];
    //sum[i] = 0;
    for (int k = 1; k < 4; k++ )  {
      //sum[i] = sum[i] + matInt[k][i];
      if (minScoreColumn[i] > matInt[k][i]) {
        minScoreColumn[i] = matInt[k][i];
      }
      if (maxScoreColumn[i] < matInt[k][i]) {
        maxScoreColumn[i] = matInt[k][i];
      }
    }
    minScore = minScore + minScoreColumn[i];
    maxScore = maxScore + maxScoreColumn[i];
    //cout << "minScoreColumn[" << i << "] = " << minScoreColumn[i] << endl;
    //cout << "maxScoreColumn[" << i << "] = " << maxScoreColumn[i] << endl;
  }
  this->scoreRange = maxScore - minScore + 1;
  
  bestScore = new long long[length];
  worstScore = new long long[length];
  bestScore[length-1] = maxScore;
  worstScore[length-1] = minScore;
  for (int i = length - 2; i >= 0; i--) {
    bestScore[i]  = bestScore[i+1]  - maxScoreColumn[i+1];
    worstScore[i] = worstScore[i+1] - minScoreColumn[i+1];
  }
  
}




/**
* Computes the pvalue associated with the threshold score requestedScore.
 */
void Matrix::lookForPvalue (long long requestedScore, long long min, long long max, double *pmin, double *pmax) {
  
  map<long long, double> *nbocc = calcDistribWithMapMinMax(min,max); 
  map<long long, double>::iterator iter;
  

  // computes p values and stores them in nbocc[length] 
  double sum = nbocc[length][max+1];
  long long s = max + 1;
  map<long long, double>::reverse_iterator riter = nbocc[length-1].rbegin();
  while (riter != nbocc[length-1].rend()) {
    sum += riter->second;
    if (riter->first >= requestedScore) s = riter->first;
    nbocc[length][riter->first] = sum;
    riter++;      
  }
  //cout << "   s found : " << s << endl;
  
  iter = nbocc[length].find(s);
  while (iter != nbocc[length].begin() && iter->first >= s - errorMax) {
    iter--;      
  }
  //cout << "   s - E found : " << iter->first << endl;
  
#ifdef MEMORYCOUNT
  // for tests, store the number of memory bloc necessary
  for (int pos = 0; pos <= length; pos++) {
    totalMapSize += nbocc[pos].size();
  }
#endif
  
  *pmax = nbocc[length][s];
  *pmin = iter->second;

  delete[] nbocc;
  delete[] minScoreColumn;
  delete[] maxScoreColumn;
  delete[] bestScore;
  delete[] worstScore;
  delete[] offsets;
  for (int k = 0; k < 4; k++) {        
      delete[] matInt[k];
    }
  delete[] matInt;
  
}



/**
* Computes the score associated with the pvalue requestedPvalue.
 */
long long Matrix::lookForScore (long long min, long long max, double requestedPvalue, double *rpv, double *rppv) {
  
  map<long long, double> *nbocc = calcDistribWithMapMinMax(min,max); 
  map<long long, double>::iterator iter;

  // computes p values and stores them in nbocc[length] 
  double sum = 0.0;
  map<long long, double>::reverse_iterator riter = nbocc[length-1].rbegin();
  long long alpha = riter->first+1;
  long long alpha_E = alpha;
  nbocc[length][alpha] = 0.0;
  while (riter != nbocc[length-1].rend()) {
    sum += riter->second;
    nbocc[length][riter->first] = sum;
    if (sum >= requestedPvalue) { 
      break;
    }
    riter++;      
  }
  if (sum > requestedPvalue) {
    alpha_E = riter->first;
    riter--;
    alpha = riter->first; 
  } else {
    if (riter == nbocc[length-1].rend()) { // path following the remark of the mail
      riter--;
      alpha = alpha_E = riter->first;
    } else {
      alpha = riter->first;
      riter++;
      sum += riter->second;
      alpha_E = riter->first;
    }
    nbocc[length][alpha_E] = sum;  
    //cout << "Pv(S) " << riter->first << " " << sum << endl;   
  } 
  
#ifdef MEMORYCOUNT
  // for tests, store the number of memory bloc necessary
  for (int pos = 0; pos <= length; pos++) {
    totalMapSize += nbocc[pos].size();
  }
#endif
  
  if (alpha - alpha_E > errorMax) alpha_E = alpha;
  
  *rpv = nbocc[length][alpha];
  *rppv = nbocc[length][alpha_E];   
  
  delete[] nbocc;
  delete[] minScoreColumn;
  delete[] maxScoreColumn;
  delete[] bestScore;
  delete[] worstScore;
  delete[] offsets;
  delete[] matInt;

  return alpha;
  
}


// computes the distribution of scores between score min and max as the DP algrithm proceeds 
// but instead of using a table we use a map to avoid computations for scores that cannot be reached
map<long long, double> *Matrix::calcDistribWithMapMinMax (long long min, long long max) { 
  
  // maps for each step of the computation
  // nbocc[length] stores the pvalue
  // nbocc[pos] for pos < length stores the qvalue
  map<long long, double> *nbocc = new map<long long, double> [length+1];
  map<long long, double>::iterator iter;
  
  long long *maxs = new long long[length+1]; // @ pos i maximum score reachable with the suffix matrix from i to length-1
  
  maxs[length] = 0;
  for (int i = length-1; i >= 0; i--) {
    maxs[i] = maxs[i+1] + maxScoreColumn[i];
  }
  
  // initializes the map at position 0
  for (int k = 0; k < 4; k++) {
    if (matInt[k][0]+maxs[1] >= min) {
      nbocc[0][matInt[k][0]] += background[k];
    }
  }
  
  // computes q values for scores greater or equal than min
  nbocc[length-1][max+1] = 0.0;
  for (int pos = 1; pos < length; pos++) {
    iter = nbocc[pos-1].begin();
    while (iter != nbocc[pos-1].end()) {
      for (int k = 0; k < 4; k++) {
        long long sc = iter->first + matInt[k][pos];
        if (sc+maxs[pos+1] >= min) {
          // the score min can be reached
          if (sc > max) {
            // the score will be greater than max for all suffixes
            nbocc[length-1][max+1] += nbocc[pos-1][iter->first] * background[k]; //pow(4,length-pos-1) ;
            totalOp++;
          } else {              
            nbocc[pos][sc] += nbocc[pos-1][iter->first] * background[k];
            totalOp++;
          }
        } 
      }
      iter++;      
    }      
    //cerr << "        map size for " << pos << " " << nbocc[pos].size() << endl;
  }
  
  delete[] maxs;
  
  return nbocc;
  
  
}




long long Matrix::fastPvalue (Matrix *m, long long alpha) {
  
  
  map<long long, long long> *q = new map<long long, long long> [m->length+1];
  map<long long, long long>::iterator iter;
  
  long long P = 0;
  
  long long *maxm = new long long[m->length+1]; // @ pos i maximum score reachable with the suffix matrix from i to length-1
  
  maxm[m->length] = 0;
  for (int i = m->length-1; i >= 0; i--) {
    maxm[i] = maxm[i+1] + m->maxScoreColumn[i];
  }
  
  // initializes the map at position 0
  for (int k = 0; k < 4; k++) {
    if (m->matInt[k][0]+maxm[1] >= alpha) {
      //cout << "FP: Set " << m->matInt[k][0] <<  " to ";
      q[0][m->matInt[k][0]] += 1;
      //cout << q[0][m->matInt[k][0]] << endl;        
    }
  }
  
  // computes q values for scores strictly greater than alpha
  for (int pos = 1; pos < m->length; pos++) {
    iter = q[pos-1].begin();
    while (iter != q[pos-1].end()) {
      for (int k = 0; k < 4; k++) {
        long long scm = iter->first + m->matInt[k][pos];
        if (scm > alpha) {
          //cout << "Update P from " << P;
          P += iter->second * (long long)pow(4.0,m->length-pos-1); 
          //cout << " to P " << P << endl;
        } else if (scm + maxm[pos+1] > alpha) {
          q[pos][scm] += iter->second; 
        }
      } 
      iter++;      
    }      
    q[pos-1].erase(q[pos-1].begin(),q[pos-1].end());
  }
  
  
  delete[] maxm;
  delete[] q;
  
  return P;
  
}

