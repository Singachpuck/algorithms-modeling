import java.util.*;
import java.util.stream.IntStream;

public class AbcBeeAlgorithm {

    private final int workerBeesCount;
    private final int scoutBeesCount;
    private final int[][] graph;
    private final Random random = new Random();

    public AbcBeeAlgorithm(int workerBeesCount, int scoutBeesCount, int[][] graph) {
        if (graph == null)
            throw new NullPointerException();

        if (graph.length == 0 || graph.length != graph[0].length)
            throw new IllegalArgumentException();

        this.workerBeesCount = workerBeesCount;
        this.scoutBeesCount = scoutBeesCount;
        this.graph = graph;
    }

    public int[] paint() {

        int colorsInUse = 0;
        int[] coloredVertices = new int[graph.length];
        PriorityQueue<Integer> toProcess = new PriorityQueue<>(scoutBeesCount,
                                                Comparator.comparingInt(v -> getNeighbours(v).size()));

        Set<Integer> processed = new HashSet<>();

        while (processed.size() != graph.length) {
            int availableBees = workerBeesCount;

            for (int i = 0; i < scoutBeesCount; i++) {
                if (processed.size() == graph.length)
                    break;

                int randomVertex = getRandomVertex(processed);
                toProcess.add(randomVertex);
                processed.add(randomVertex);
            }

            for (int currentVertex : toProcess) {
                Set<Integer> neighbours = getNeighbours(currentVertex);

                int neighboursToProcess = Math.min(availableBees, neighbours.size());

                for (int neighbour : neighbours) {
                    if (neighboursToProcess == 0)
                        break;

                    if (processed.contains(neighbour))
                        continue;

                    for (int j = 1; j <= colorsInUse; j++) {
                        if (isColorValid(j, neighbour, coloredVertices)) {
                            coloredVertices[neighbour] = j;
                            processed.add(neighbour);
                            break;
                        }
                    }

                    if (coloredVertices[neighbour] == 0) {
                        coloredVertices[neighbour] = ++colorsInUse;
                    }

                    neighboursToProcess--;
                }

                for (int j = 1; j <= colorsInUse; j++) {
                    if (isColorValid(j, currentVertex, coloredVertices)) {
                        coloredVertices[currentVertex] = j;
                        processed.add(currentVertex);
                        break;
                    }
                }

                if (coloredVertices[currentVertex] == 0) {
                    coloredVertices[currentVertex] = ++colorsInUse;
                }

                availableBees = Math.max(availableBees - neighbours.size(), 0);
            }

        }

        return coloredVertices;
    }

    private boolean isColorValid(int color, int vertex, int[] coloredVertices) {
        for (int neighbour : getNeighbours(vertex)) {
            if (coloredVertices[neighbour] == color)
                return false;
        }

        return true;
    }

    private Set<Integer> getNeighbours(int vertex) {
        return IntStream.range(0, graph.length)
                .filter(v -> graph[vertex][v] == 1)
                .collect(HashSet::new, HashSet::add, AbstractCollection::addAll);
    }

    private int getRandomVertex(Set<Integer> processedVertices) {
        int[] availableVertices = IntStream.range(0, graph.length)
                .filter(vertex -> !processedVertices.contains(vertex)).toArray();

        return availableVertices[random.nextInt(availableVertices.length)];
    }
}
