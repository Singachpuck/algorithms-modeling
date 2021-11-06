import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class BeeAlgorithmTest {

    @Test
    void printTest() {

        final int workerBeesCount = 27;
        final int scoutBeesCount = 4;
        final int[][] adjucencyMatrix = {
                {0, 1, 1, 0, 0, 0, 0, 0, 0, 1},
                {1, 0, 0, 1, 0, 0, 0, 0, 0, 1},
                {1, 0, 0, 0, 0, 1, 0, 0, 0, 1},
                {0, 1, 0, 0, 1, 1, 0, 0, 0, 0},
                {0, 0, 0, 1, 0, 1, 1, 0, 1, 1},
                {0, 0, 1, 1, 1, 0, 1, 0, 0, 0},
                {0, 0, 0, 0, 1, 1, 0, 1, 1, 0},
                {0, 0, 0, 0, 0, 0, 1, 0, 1, 0},
                {0, 0, 0, 0, 1, 0, 1, 1, 0, 1},
                {1, 1, 1, 0, 1, 0, 0, 0, 1, 0}
        };

        BeeAlgorithm beeAlgorithm = new BeeAlgorithm(adjucencyMatrix, workerBeesCount, scoutBeesCount);

        System.out.println(Arrays.toString(beeAlgorithm.paint()));
    }

}