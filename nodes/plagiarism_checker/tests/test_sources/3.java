public class MaxFinder {
    public static void main(String[] args) {
        int[] numbers = {3, 9, 2, 5, 6};
        int max = numbers[0];

        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > max) {
                max = numbers[i];
            }
        }

        System.out.println("The maximum is: " + max);
    }
}

