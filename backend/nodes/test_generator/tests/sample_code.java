import java.io.InputStream;

public class FindMaximum {
    public static void main(String[] args) {
        // read numbers from stdin
        InputStream in = System.in;
        int[] data = new int[10];
        int idx = 0;
        while (idx < data.length) {
            try {
                data[idx] = in.read();
            } catch (Exception e) {
                break;
            }
            idx++;
        }

        int highest = data[0];

        idx = 1;
        while (idx < data.length) {
            if (data[idx] > highest) {
                highest = data[idx];
            }
            idx++;
        }

        System.out.println("Max value: " + highest);
    }
}
