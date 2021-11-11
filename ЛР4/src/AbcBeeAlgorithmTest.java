import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class AbcBeeAlgorithmTest {

    @Test
    void paintTest() {

        final int workerBeesCount = 27;
        final int scoutBeesCount = 3;
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

        final int iterations = 100;

        AbcBeeAlgorithm abcBeeAlgorithm = new AbcBeeAlgorithm(workerBeesCount, scoutBeesCount, adjucencyMatrix);

        int chromaticNumber = Integer.MAX_VALUE;

        for (int i = 0; i < iterations; i++) {
            int cn = Arrays.stream(abcBeeAlgorithm.paint()).max().getAsInt();

            if (cn < chromaticNumber) {
                chromaticNumber = cn;
            }
        }

        assertEquals(chromaticNumber, 3);
    }
}