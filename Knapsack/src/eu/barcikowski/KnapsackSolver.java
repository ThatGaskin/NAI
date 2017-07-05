package eu.barcikowski;

/**
 * Created by GaskinPC on 28.05.2017.
 */

import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

/**
 * Class <code>KnapsackSolver</code> implements greedy way(hill climb) to solve knapsack problem.
 */
public class KnapsackSolver {

    private static int[] taken;
    private static int value = 0;
    private static int[] values;
    private static int[] weights;
    static int items;
    private static int capacity;

    public static void main(String[] args) {
        try {

            knapsackSolver(args);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Read the file, , solve it, and print the solution in the standard output
     */
    private static void knapsackSolver(String[] args) throws IOException {
        String fileName = null;

        for (String arg : args) {
            if (arg.startsWith("-file=")) {
                fileName = arg.substring(6);
            }
        }
        if (fileName == null)
            return;
        List<String> lines = new ArrayList<>();

        try (BufferedReader input = new BufferedReader(new FileReader(fileName))) {
            String line = null;
            while ((line = input.readLine()) != null) {
                lines.add(line);
            }
        }

        // parse the data in the file
        capacity = Integer.parseInt(lines.get(0));
        items = lines.size() - 1;
        values = new int[items];
        weights = new int[items];

        for (int i = 1; i < items + 1; i++) {
            String line = lines.get(i);
            String[] parts = line.split("\\s+");

            values[i - 1] = Integer.parseInt(parts[0]);
            weights[i - 1] = Integer.parseInt(parts[1]);
        }


        taken = new int[items];
        int maxTries = 20000;

        //making start/random node:
        System.out.print("Starting vector:   ");
        for (int i = 0; i < items; i++) {
            double a = Math.random();
            if (a < 0.5)
                taken[i] = 1;
        }

        Node origin1 = new Node();
        origin1.value = score(taken);
        value = origin1.value;
        origin1.takenItems = taken;


        System.out.println(Arrays.toString(origin1.takenItems) + " | New value:" + origin1.value);


        Node origin = new Node();
        origin.value = score(taken);
        value = origin.value;
        origin.takenItems = taken;

        for (int i = 0; i < maxTries; i++) {

            Node n = stepOver(origin);
            if (n != origin) {
                System.out.println("Vector changed: " + Arrays.toString(n.takenItems) + " | New value:" + n.value);
            }
            origin = n;
        }

        System.out.println("Final value of knapsack: " + origin.value);
        System.out.println("Final vector: " + Arrays.toString(origin.takenItems) + " | New value:" + origin.value);

    }

    /**
     * Class <code>Node</code> represents single state of knapsack.
     */
    public static class Node {
        int value;
        int[] takenItems = new int[items];

        @Override
        public String toString() {
            return "\n" + value + "\n" + Arrays.toString(takenItems) + "\n";
        }
    }

    /**
     * Attempt to find a neighbour node with better value
     *
     * @param oldN
     * @return node with better value or orgin node if found neighbour had lower value
     */

    public static Node stepOver(Node oldN) {
        Node n = generateNeighbours(oldN);

        int currentValue = score(n.takenItems);
        n.value = currentValue;
        if (currentValue > value) {
            taken = n.takenItems;
            value = n.value;
            return n;
        } else if (currentValue > oldN.value) {
            return n;
        } else {
            return oldN;
        }

    }

    /**
     * Generate a node thats simmilar to the orginNode
     *
     * @param oldN
     * @return node that is somewhat similar to orginNode
     */


    private static Node generateNeighbours(Node oldN) {

        Node n = new Node();
        for (int i = 0; i < items; i++) {
            double a = Math.random();
            if (a < 1 / (double) items)
                n.takenItems[i] = 1 - oldN.takenItems[i];
            else
                n.takenItems[i] = oldN.takenItems[i];
        }


        return n;
    }

    /**
     * Check the value of current takenItems vector
     *
     * @param taken
     * @return value of given node, 0 if the weight extends capacity
     */

    private static int score(int[] taken) {
        int weight = 0;
        int currentValue = 0;
        for (int i = 0; i < items; i++) {
            weight += taken[i] * weights[i];
            currentValue += taken[i] * values[i];
        }
        if (weight > capacity) return -1;
        return currentValue;
    }


}
