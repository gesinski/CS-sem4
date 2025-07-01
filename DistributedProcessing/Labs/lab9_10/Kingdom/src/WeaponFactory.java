import Resources.*;
public class WeaponFactory extends Thread {
    private final ResourceStore<Coal> coalStore;
    private final ResourceStore<Ore> oreStore;
    private final ResourceStore<Weapon> weaponStore;

    public WeaponFactory(ResourceStore<Coal> coalStore, ResourceStore<Ore> oreStore, ResourceStore<Weapon> weaponStore) {
        this.coalStore = coalStore;
        this.oreStore = oreStore;
        this.weaponStore = weaponStore;
    }

    @Override
    public void run() {
        try {
            while (true) {
                for (int i = 0; i < 2; i++) coalStore.consume();
                for (int i = 0; i < 3; i++) oreStore.consume();
                weaponStore.produce(new Weapon());
                Thread.sleep(2000);
            }
        } catch (InterruptedException ignored) {}
    }
}
