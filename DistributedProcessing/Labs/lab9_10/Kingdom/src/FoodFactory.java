import Resources.*;
public class FoodFactory extends Thread {
    private final ResourceStore<Coal> coalStore;
    private final ResourceStore<Food> foodStore;

    public FoodFactory(ResourceStore<Coal> coalStore, ResourceStore<Ore> oreStore, ResourceStore<Food> foodStore) {
        this.coalStore = coalStore;
        this.foodStore = foodStore;
    }

    @Override
    public void run() {
        try {
            while (true) {
                for (int i = 0; i < 4; i++) coalStore.consume();
                foodStore.produce(new Food());
                Thread.sleep(2000);
            }
        } catch (InterruptedException ignored) {}
    }
}
