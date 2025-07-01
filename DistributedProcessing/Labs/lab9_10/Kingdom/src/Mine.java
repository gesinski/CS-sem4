import Resources.Coal;
import Resources.Ore;

import java.util.Random;

public class Mine extends Thread {
    private final ResourceStore<Coal> coalStore;
    private final ResourceStore<Ore> oreStore;
    private final Random random = new Random();

    public Mine(ResourceStore<Coal> coalStore, ResourceStore<Ore> oreStore) {
        this.coalStore = coalStore;
        this.oreStore = oreStore;
    }

    @Override
    public void run() {
        try {
            while (true) {
                int coalAmount = 1 + random.nextInt(3);
                int oreAmount = 1 + random.nextInt(3);

                for (int i = 0; i < oreAmount; i++) {
                    oreStore.produce(new Ore());
                }
                for (int i = 0; i < coalAmount; i++) {
                    coalStore.produce(new Coal());
                }

                Thread.sleep(1000 + random.nextInt(1000));
            }
        } catch (InterruptedException ignored) {}
    }
}
