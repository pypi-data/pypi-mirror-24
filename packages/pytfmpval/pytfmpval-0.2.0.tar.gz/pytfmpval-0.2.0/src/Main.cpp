//There is no justice in this world

#include "Matrix.h"


int main() {
    // std::cout << "whoa nelly" << std::endl;

    Matrix m;
    // string counts = "17  30  5   7   42  41  21  0   13  22  20  32  6   7   32  33  42  18  5   23  27  29 5   4   0   0   2   3   0   18  8   2   2   0   2   25  0   2   0   0   6   6   3   1 14  0   0   0   0   0   1   10  19  16  7   4   4   2   0   0   0   2   4   1   0   3 8   10  39  37  0   0   22  16  4   4   15  8   32  10  12  9   2   24  29  14  14  11";
    string counts = "3  7  9  3 11 11 11  3  4  3  8  8  9  9 11  2 5  0  1  6  0  0  0  3  1  4  5  1  0  5  0  7 4  3  1  4  3  2  2  2  8  6  1  4  2  0  3  0 2  4  3  1  0  1  1  6  1  1  0  1  3  0  0  5";
    m.readMatrix(counts);
    m.toLogOddRatio();
    double initialGranularity = 0.1;
    bool forcedGranularity = false; 
    double maxGranularity = 1e-9;
    long long max;
    long long min;
    double ppv;
    double pv;
    long long score;
    double requestedScore = 2;

    long long totalSize;
    long long totalOp;
    totalSize = 0;
    totalOp = 0;
  
    for (double granularity = initialGranularity; granularity >= maxGranularity; granularity /= 10) {

        std::cout << "Computing rounded matrix with granularity " << granularity << std::endl;

        m.computesIntegerMatrix(granularity);
        max = requestedScore*m.granularity + m.offset + m.errorMax+1;
        min = requestedScore*m.granularity + m.offset - m.errorMax-1;
        score = requestedScore*m.granularity + m.offset;
        

        std::cout << "Score range : " << m.scoreRange << std::endl;
        std::cout << "Min         : " << min << std::endl;
        std::cout << "Max         : " << max << std::endl;
        std::cout << "Precision   : " << m.granularity << std::endl;
        std::cout << "Error max   : " << m.errorMax << std::endl;
        std::cout << "Computing pvalue for requested score " << requestedScore << " " << score << std::endl;

        
          
        // computes pvalues for reachable score in range min - max    
        m.totalMapSize = 0;
        m.totalOp = 0;

        
        m.lookForPvalue(score,min,max,&ppv,&pv);
        

        std::cout << "Prev. Pvalue  : " << ppv << std::endl;
        std::cout << "Pvaluex       : " << pv << std::endl;
        std::cout << "Comp. score   : " << score << std::endl;

        totalSize += m.totalMapSize;
        totalOp += m.totalOp;
        
        std::cout << "***********************************************" << std::endl;
        
        if (ppv == pv) {
          std::cout << "#####  STOP score computed  #####" << std::endl;
          if (!forcedGranularity) {
            std::cout << "Calculated p-value: " << pv << std::endl;
            std::cout << "Total Map Size: " << totalSize << std::endl;
            std::cout << "Total OP: " << totalOp << std::endl;
            break;
          }
        }
        
      }

}