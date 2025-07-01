import Resources.Resource;

import java.util.LinkedList;
import java.util.Queue;

public class ResourceStore<T> {
    private final LinkedList<T> resources = new LinkedList<>();
    private final int capacity;
    private int totalProduced = 0;
    private int totalConsumed = 0;

    public ResourceStore(int capacity) {
        this.capacity = capacity;
    }

    public synchronized void produce(T item) throws InterruptedException {
        while (resources.size() >= capacity) {
            wait();
        }
        resources.add(item);
        totalProduced++;
        notifyAll();
    }

    public synchronized T consume() throws InterruptedException {
        while (resources.isEmpty()) {
            wait();
        }
        T res = resources.poll();
        totalConsumed++;
        notifyAll();
        return res;
    }

    public synchronized int getSize() {
        return resources.size();
    }

    public synchronized int getTotalProduced() {
        return totalProduced;
    }

    public synchronized int getTotalConsumed() {
        return totalConsumed;
    }
}
