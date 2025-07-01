import Resources.*;

public class Main {
    public static void main(String[] args) {
        KingdomGUI gui = new KingdomGUI();
        gui.setVisible(true);
        // === Królestwo A ===
        ResourceStore<Coal> coalStoreA = new ResourceStore<>(20);
        ResourceStore<Ore> oreStoreA = new ResourceStore<>(20);
        ResourceStore<Jewelry> jewelryStoreA = new ResourceStore<>(10);
        ResourceStore<Happiness> happinessStoreA = new ResourceStore<>(10);
        ResourceStore<Weapon> weaponStoreA = new ResourceStore<>(10);
        ResourceStore<Food> foodStoreA = new ResourceStore<>(10);
        ResourceStore<Tactics> tacticsStoreA = new ResourceStore<>(10);

        new Mine(coalStoreA, oreStoreA).start();
        new JewelryFactory(coalStoreA, oreStoreA, jewelryStoreA).start();
        new WeaponFactory(coalStoreA, oreStoreA, weaponStoreA).start();
        new FoodFactory(coalStoreA, oreStoreA, foodStoreA).start();
        new Princess(jewelryStoreA, happinessStoreA).start();
        new King(happinessStoreA, tacticsStoreA).start();
        Army armyA = new Army(weaponStoreA, foodStoreA, tacticsStoreA);
        armyA.start();

        new KingdomStatsDisplay(
                "A",
                coalStoreA, oreStoreA, jewelryStoreA,
                foodStoreA, weaponStoreA, happinessStoreA,
                tacticsStoreA, armyA, gui
        ).start();

        // === Królestwo B ===
        ResourceStore<Coal> coalStoreB = new ResourceStore<>(20);
        ResourceStore<Ore> oreStoreB = new ResourceStore<>(20);
        ResourceStore<Jewelry> jewelryStoreB = new ResourceStore<>(10);
        ResourceStore<Happiness> happinessStoreB = new ResourceStore<>(10);
        ResourceStore<Weapon> weaponStoreB = new ResourceStore<>(10);
        ResourceStore<Food> foodStoreB = new ResourceStore<>(10);
        ResourceStore<Tactics> tacticsStoreB = new ResourceStore<>(10);

        new Mine(coalStoreB, oreStoreB).start();
        new JewelryFactory(coalStoreB, oreStoreB, jewelryStoreB).start();
        new WeaponFactory(coalStoreB, oreStoreB, weaponStoreB).start();
        new FoodFactory(coalStoreB, oreStoreB, foodStoreB).start();
        new Princess(jewelryStoreB, happinessStoreB).start();
        new King(happinessStoreB, tacticsStoreB).start();
        Army armyB = new Army(weaponStoreB, foodStoreB, tacticsStoreB);
        armyB.start();

        new KingdomStatsDisplay(
                "B",
                coalStoreB, oreStoreB, jewelryStoreB,
                foodStoreB, weaponStoreB, happinessStoreB,
                tacticsStoreB, armyB, gui
        ).start();

        // === Monitor wojny ===
        new WarMonitor(armyA, armyB).start();
    }
}
