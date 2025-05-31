public class FindMaximum {
    public static void main(String[] args) {
        int[] data = {3, 9, 2, 5, 6};
        int highest = data[0];

        int idx = 1;
        while (idx < data.length) {
            if (data[idx] > highest) {
                highest = data[idx];
            }
            idx++;
        }

        System.out.println("Max value: " + highest);
    }
}
