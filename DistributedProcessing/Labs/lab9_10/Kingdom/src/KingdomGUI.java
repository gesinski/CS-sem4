import javax.swing.*;
import java.awt.*;

public class KingdomGUI extends JFrame {
    private final JTextArea statusA;
    private final JTextArea statusB;

    public KingdomGUI() {
        setTitle("Kingdom Status Viewer");
        setSize(600, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        statusA = new JTextArea();
        statusA.setEditable(false);
        statusA.setBorder(BorderFactory.createTitledBorder("Kingdom A"));

        statusB = new JTextArea();
        statusB.setEditable(false);
        statusB.setBorder(BorderFactory.createTitledBorder("Kingdom B"));

        setLayout(new GridLayout(1, 2));
        add(new JScrollPane(statusA));
        add(new JScrollPane(statusB));
    }

    public void updateStatus(String kingdom, String status) {
        SwingUtilities.invokeLater(() -> {
            if (kingdom.equals("A")) {
                statusA.setText(status);
            } else if (kingdom.equals("B")) {
                statusB.setText(status);
            }
        });
    }


    public static void main(String[] args) {
        KingdomGUI gui = new KingdomGUI();
        gui.setVisible(true);

        // Example: simulate updating status every second
        new Thread(() -> {
            int a = 0, b = 0;
            while (true) {
                String statusA = "Coal: " + (int)(Math.random()*20) +
                        "\nOre: " + (int)(Math.random()*20) +
                        "\nJewelry: " + (int)(Math.random()*10) +
                        "\nArmy: " + (a++);
                String statusB = "Coal: " + (int)(Math.random()*20) +
                        "\nOre: " + (int)(Math.random()*20) +
                        "\nJewelry: " + (int)(Math.random()*10) +
                        "\nArmy: " + (b++);

                gui.updateStatus("A", statusA);
                gui.updateStatus("B", statusB);

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
}
