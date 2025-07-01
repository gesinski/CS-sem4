import Resources.*;
public class JewelryFactory extends Thread {
    private final ResourceStore<Ore> oreStore;
    private final ResourceStore<Jewelry> jewelryStore;

    public JewelryFactory(ResourceStore<Coal> coalStore, ResourceStore<Ore> oreStore, ResourceStore<Jewelry> jewelryStore) {
        this.oreStore = oreStore;
        this.jewelryStore = jewelryStore;
    }

    @Override
    public void run() {
        try {
            while (true) {
                for (int i = 0; i < 3; i++) oreStore.consume();
                jewelryStore.produce(new Jewelry());
                Thread.sleep(1000);
            }
        } catch (InterruptedException ignored) {}
    }
}
