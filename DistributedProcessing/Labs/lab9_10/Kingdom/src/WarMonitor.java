public class WarMonitor extends Thread {
    private final Army armyA;
    private final Army armyB;
    private final int winningArg = 15;

    public WarMonitor(Army armyA, Army armyB) {
        this.armyA = armyA;
        this.armyB = armyB;
    }

    @Override
    public void run() {
        try {
            while (true) {
                int countA = armyA.getUnitsProduced();
                int countB = armyB.getUnitsProduced();

                System.out.println("[WarMonitor] Kingdom A: " + countA + " units, Kingdom B: " + countB + " units");

                if (countA >= winningArg || countB >= winningArg) {
                    if (countA >= winningArg && countB >= winningArg)
                        System.out.println("🤝 It's a draw! Both kingdoms reached 100 units.");
                    else if (countA >= winningArg)
                        System.out.println("🏆 Kingdom A WINS THE WAR!");
                    else
                        System.out.println("🏆 Kingdom B WINS THE WAR!");

                    // zatrzymaj armie
                    armyA.stopArmy();
                    armyB.stopArmy();
                    System.exit(0);  // zakończ program
                }

                Thread.sleep(1000);
            }
        } catch (InterruptedException ignored) {}
    }
}
