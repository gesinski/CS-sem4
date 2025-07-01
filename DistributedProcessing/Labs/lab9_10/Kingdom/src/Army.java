import Resources.*;
public class Army extends Thread {
    private final ResourceStore<Weapon> weaponStore;
    private final ResourceStore<Food> foodStore;
    private final ResourceStore<Tactics> tacticsStore;

    private int unitsProduced = 0;
    private boolean running = true;

    public Army(ResourceStore<Weapon> weaponStore, ResourceStore<Food> foodStore, ResourceStore<Tactics> tacticsStore) {
        this.weaponStore = weaponStore;
        this.foodStore = foodStore;
        this.tacticsStore = tacticsStore;
    }

    @Override
    public void run() {
        try {
            while (running) {
                weaponStore.consume();
                foodStore.consume();
                tacticsStore.consume();
                unitsProduced++;
                System.out.println("[Army] Unit created. Total: " + unitsProduced);
                Thread.sleep(4000);
            }
        } catch (InterruptedException ignored) {}
    }

    public int getUnitsProduced() {
        return unitsProduced;
    }

    public void stopArmy() {
        running = false;
    }
}
