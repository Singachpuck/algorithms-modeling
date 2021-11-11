import java.util.*;
import java.util.stream.IntStream;

public class BeeAlgorithm {

    private final int[][] graph;
    private final int workerBeesCount;
    private final int scoutBeesCount;
    private final Random random;

    public BeeAlgorithm(int[][] graph, int workerBeesCount, int scoutBeesCount) {
        if (graph == null)
            throw new NullPointerException();

        if (graph.length == 0 || graph.length != graph[0].length)
            throw new IllegalArgumentException();

        this.graph = graph;
        this.workerBeesCount = workerBeesCount;
        this.scoutBeesCount = scoutBeesCount;
        this.random = new Random();
    }

    public int[] paint() {
        int colorsInUse = 0;
        int[] coloredVertices = greedyPaint();
        HashSet<Integer> processedVertices = new HashSet<>();
        int availableBees = workerBeesCount;

        while (processedVertices.size() != graph.length) {
            List<Integer> toProcess = new ArrayList<>();

            for (int i = 0; i < scoutBeesCount; i++) {
                if (processedVertices.size() == graph.length)
                    break;

                int randomVertex = getRandomVertex(processedVertices);
                toProcess.add(randomVertex);
                processedVertices.add(randomVertex);
            }

            toProcess.sort(Comparator.comparingInt(this::getDegree).reversed());

            for (Integer vertex : toProcess) {
                Set<Integer> neighbours = getNeighbours(vertex);

                int processVertices = Math.min(availableBees, neighbours.size());
                int i = 0;

                for (int neighbour : neighbours) {
                    if (i == processVertices)
                        break;

                    List<Integer> colorCount = countColors(coloredVertices);

                    if (trySwapColor(vertex, neighbour, coloredVertices)) {

                        for (int j = 1; j <= colorCount.size(); j++) {

                            if (isColorValid(j, vertex, coloredVertices)
                                    && colorCount.get(coloredVertices[vertex] - 1) < colorCount.get(j - 1)) {
                                coloredVertices[vertex] = j;
                                colorCount = countColors(coloredVertices);
                            }

                            if (isColorValid(j, neighbour, coloredVertices)
                                    && colorCount.get(coloredVertices[neighbour] - 1) < colorCount.get(j - 1)) {
                                coloredVertices[neighbour] = j;
                                colorCount = countColors(coloredVertices);
                            }

                        }
                    }

                    i++;
                }

                availableBees = Math.max(availableBees - neighbours.size(), 0);
            }
        }

        return coloredVertices;
    }

    private List<Integer> countColors(int[] coloredVertices) {
        List<Integer> colorsCount = new ArrayList<>();

        for (int color : coloredVertices) {
            while (colorsCount.size() <= (color - 1)) {
                colorsCount.add(0);
            }

            colorsCount.set(color - 1, colorsCount.get(color - 1) + 1);
        }

        return colorsCount;
    }

    private boolean trySwapColor(int v1, int v2, int[] coloredVertices) {
        if (isColorValidNoConsider(coloredVertices[v1], v2, coloredVertices, v1)
                && isColorValidNoConsider(coloredVertices[v2], v1, coloredVertices, v2)) {
            int tmp = coloredVertices[v1];
            coloredVertices[v1] = coloredVertices[v2];
            coloredVertices[v2] = tmp;
            return true;
        }

        return false;
    }

    private int getDegree(int vertex) {
        return (int) IntStream.range(0, graph.length)
                            .filter(v -> graph[vertex][v] == 1).count();
    }

    public int[] greedyPaint() {
        int color = 0;
        int[] coloredVertices = new int[graph.length];
        HashSet<Integer> processedVertices = new HashSet<>();
        int currentVertex = 0;

        while (processedVertices.size() != graph.length) {
            color++;

            recursivePaint(color, coloredVertices, processedVertices, currentVertex);

            do {
                currentVertex++;
            } while (processedVertices.contains(currentVertex));
        }

        return coloredVertices;
    }

    private void recursivePaint(int color, int[] coloredVertices, Set<Integer> processedVertices, int currentVertex) {

        if (!isColorValid(color, currentVertex, coloredVertices) || processedVertices.contains(currentVertex))
            return;

        coloredVertices[currentVertex] = color;
        processedVertices.add(currentVertex);

        for (int neighbour : getNeighbours(currentVertex)) {

            for (int neighbourNeighbour : getNeighbours(neighbour)) {

                if (!processedVertices.contains(neighbourNeighbour)) {
                    recursivePaint(color, coloredVertices, processedVertices, neighbourNeighbour);
                }
            }
        }
    }

    private boolean isColorValidNoConsider(int color, int vertex, int[] coloredVertices, int notConsider) {
        for (int neighbour : getNeighbours(vertex)) {
            if (notConsider == neighbour)
                continue;

            if (coloredVertices[neighbour] == color)
                return false;
        }

        return true;
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
