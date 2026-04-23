import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class FindMaximum {
    public static void main(String[] args) {
        Scanner reader = new Scanner(System.in);
        List<Integer> data = new ArrayList<>();
        int n = reader.nextInt();
        for (int i = 0; i < n; i++) {
            data.add(reader.nextInt());
        }

        int highest = data.get(0);

        for (int i = 1; i < data.size(); i++) {
            if (data.get(i) > highest) {
                highest = data.get(i);
            }
        }

        System.out.println("Max value: " + highest);
    }
}
