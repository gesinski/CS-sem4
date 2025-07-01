import Resources.*;
public class KingdomStatsDisplay extends Thread {
    private final String kingdomId;
    private final ResourceStore<?>[] stores;
    private final Army army;
    private final KingdomGUI gui;

    public KingdomStatsDisplay(String kingdomId,
                               ResourceStore<?> coal, ResourceStore<?> ore, ResourceStore<?> jewelry,
                               ResourceStore<?> food, ResourceStore<?> weapon, ResourceStore<?> happiness,
                               ResourceStore<?> tactics, Army army, KingdomGUI gui) {
        this.kingdomId = kingdomId;
        this.stores = new ResourceStore[]{coal, ore, jewelry, food, weapon, happiness, tactics};
        this.army = army;
        this.gui = gui;
        setName("StatsDisplay-" + kingdomId);
    }

    @Override
    public void run() {
        while (true) {
            StringBuilder sb = new StringBuilder();
            sb.append("Coal: ").append(stores[0].getSize())
                    .append(" (produced: ").append(stores[0].getTotalProduced())
                    .append(", consumed: ").append(stores[0].getTotalConsumed()).append(")\n");

            sb.append("Ore: ").append(stores[1].getSize())
                    .append(" (produced: ").append(stores[1].getTotalProduced())
                    .append(", consumed: ").append(stores[1].getTotalConsumed()).append(")\n");

            sb.append("Jewelry: ").append(stores[2].getSize())
                    .append(" (produced: ").append(stores[2].getTotalProduced())
                    .append(", consumed: ").append(stores[2].getTotalConsumed()).append(")\n");

            sb.append("Food: ").append(stores[3].getSize())
                    .append(" (produced: ").append(stores[3].getTotalProduced())
                    .append(", consumed: ").append(stores[3].getTotalConsumed()).append(")\n");

            sb.append("Weapon: ").append(stores[4].getSize())
                    .append(" (produced: ").append(stores[4].getTotalProduced())
                    .append(", consumed: ").append(stores[4].getTotalConsumed()).append(")\n");

            sb.append("Happiness: ").append(stores[5].getSize())
                    .append(" (produced: ").append(stores[5].getTotalProduced())
                    .append(", consumed: ").append(stores[5].getTotalConsumed()).append(")\n");

            sb.append("Tactics: ").append(stores[6].getSize())
                    .append(" (produced: ").append(stores[6].getTotalProduced())
                    .append(", consumed: ").append(stores[6].getTotalConsumed()).append(")\n");

            sb.append("Army units: ").append(army.getUnitsProduced()).append("\n");

            gui.updateStatus(kingdomId, sb.toString());

            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {}
        }
    }
}
