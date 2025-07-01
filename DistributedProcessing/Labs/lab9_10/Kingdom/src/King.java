import Resources.*;
public class King extends Thread {
    private final ResourceStore<Happiness> happinessStore;
    private final ResourceStore<Tactics> tacticsStore;

    public King(ResourceStore<Happiness> happinessStore, ResourceStore<Tactics> tacticsStore) {
        this.happinessStore = happinessStore;
        this.tacticsStore = tacticsStore;
    }

    @Override
    public void run() {
        try {
            while (true) {
                Happiness h = happinessStore.consume();
                tacticsStore.produce(new Tactics());
                Thread.sleep(2500);
            }
        } catch (InterruptedException ignored) {}
    }
}
