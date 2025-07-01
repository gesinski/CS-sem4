import Resources.*;
public class Princess extends Thread {
    private final ResourceStore<Jewelry> jewelryStore;
    private final ResourceStore<Happiness> happinessStore;

    public Princess(ResourceStore<Jewelry> jewelryStore, ResourceStore<Happiness> happinessStore) {
        this.jewelryStore = jewelryStore;
        this.happinessStore = happinessStore;
    }

    @Override
    public void run() {
        try {
            while (true) {
                Jewelry jewel = jewelryStore.consume();
                // transform
                happinessStore.produce(new Happiness());
                Thread.sleep(3000);
            }
        } catch (InterruptedException ignored) {}
    }
}
