// Inserting a key on a B-tree in Java

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class BTree {

    private final int T;

    public class Node {
        int n;
        int[] key = new int[2 * T - 1];
        Node[] child = new Node[2 * T];
        boolean leaf = true;

        public int Find(int k) {
            for (int i = 0; i < this.n; i++) {
                if (this.key[i] == k) {
                    return i;
                }
            }
            return -1;
        }

        public List<Integer> traverse() {

            List<Integer> items = new ArrayList<>();

            int i;
            for (i = 0; i < this.n; i++) {

                if (!this.leaf) {
                    items.addAll(child[i].traverse());
                }
                items.add(key[i]);
            }

            if (!leaf)
                items.addAll(child[i].traverse());

            return items;
        }
    }

    public BTree(int t) {
        T = t;
        root = new Node();
        root.n = 0;
        root.leaf = true;
    }

    private Node root;

    private void split(Node x, int pos, Node y) {
        Node z = new Node();
        z.leaf = y.leaf;
        z.n = T - 1;
        for (int j = 0; j < T - 1; j++) {
            z.key[j] = y.key[j + T];
        }
        if (!y.leaf) {
            for (int j = 0; j < T; j++) {
                z.child[j] = y.child[j + T];
            }
        }
        y.n = T - 1;
        for (int j = x.n; j >= pos + 1; j--) {
            x.child[j + 1] = x.child[j];
        }
        x.child[pos + 1] = z;

        for (int j = x.n - 1; j >= pos; j--) {
            x.key[j + 1] = x.key[j];
        }
        x.key[pos] = y.key[T - 1];
        x.n = x.n + 1;
    }

    public void insert(final int key) {
        Node r = root;
        if (r.n == 2 * T - 1) {
            Node s = new Node();
            root = s;
            s.leaf = false;
            s.n = 0;
            s.child[0] = r;
            split(s, 0, r);
            _insert(s, key);
        } else {
            _insert(r, key);
        }
    }

    private void _insert(Node x, int k) {

        if (x.leaf) {
            int i = 0;
            for (i = x.n - 1; i >= 0 && k < x.key[i]; i--) {
                x.key[i + 1] = x.key[i];
            }
            x.key[i + 1] = k;
            x.n = x.n + 1;
        } else {
            int i = 0;
            for (i = x.n - 1; i >= 0 && k < x.key[i]; i--) {
            }

            i++;
            Node tmp = x.child[i];
            if (tmp.n == 2 * T - 1) {
                split(x, i, tmp);
                if (k > x.key[i]) {
                    i++;
                }
            }
            _insert(x.child[i], k);
        }

    }

    private void remove(Node x, int key) {
        int pos = x.Find(key);
        if (pos != -1) {
            if (x.leaf) {
                int i = 0;
                for (i = 0; i < x.n && x.key[i] != key; i++) {
                }
                for (; i < x.n; i++) {
                    if (i != 2 * T - 2) {
                        x.key[i] = x.key[i + 1];
                    }
                }
                x.n--;
                return;
            }

            Node pred = x.child[pos];
            int predKey = 0;
            if (pred.n >= T) {
                for (;;) {
                    if (pred.leaf) {
                        System.out.println(pred.n);
                        predKey = pred.key[pred.n - 1];
                        break;
                    } else {
                        pred = pred.child[pred.n];
                    }
                }
                remove(pred, predKey);
                x.key[pos] = predKey;
                return;
            }

            Node nextNode = x.child[pos + 1];
            if (nextNode.n >= T) {
                int nextKey = nextNode.key[0];
                if (!nextNode.leaf) {
                    nextNode = nextNode.child[0];
                    for (;;) {
                        if (nextNode.leaf) {
                            nextKey = nextNode.key[nextNode.n - 1];
                            break;
                        } else {
                            nextNode = nextNode.child[nextNode.n];
                        }
                    }
                }
                remove(nextNode, nextKey);
                x.key[pos] = nextKey;
                return;
            }

            int temp = pred.n + 1;
            pred.key[pred.n++] = x.key[pos];
            for (int i = 0, j = pred.n; i < nextNode.n; i++) {
                pred.key[j++] = nextNode.key[i];
                pred.n++;
            }
            for (int i = 0; i < nextNode.n + 1; i++) {
                pred.child[temp++] = nextNode.child[i];
            }

            x.child[pos] = pred;
            for (int i = pos; i < x.n; i++) {
                if (i != 2 * T - 2) {
                    x.key[i] = x.key[i + 1];
                }
            }
            for (int i = pos + 1; i < x.n + 1; i++) {
                if (i != 2 * T - 1) {
                    x.child[i] = x.child[i + 1];
                }
            }
            x.n--;
            if (x.n == 0) {
                if (x == root) {
                    root = x.child[0];
                }
                x = x.child[0];
            }
            remove(pred, key);
            return;
        } else {
            for (pos = 0; pos < x.n; pos++) {
                if (x.key[pos] > key) {
                    break;
                }
            }
            Node tmp = x.child[pos];
            if (tmp.n >= T) {
                remove(tmp, key);
                return;
            }
            Node nb;
            int divider = -1;

            if (pos != x.n && x.child[pos + 1].n >= T) {
                divider = x.key[pos];
                nb = x.child[pos + 1];
                x.key[pos] = nb.key[0];
                tmp.key[tmp.n++] = divider;
                tmp.child[tmp.n] = nb.child[0];
                for (int i = 1; i < nb.n; i++) {
                    nb.key[i - 1] = nb.key[i];
                }
                for (int i = 1; i <= nb.n; i++) {
                    nb.child[i - 1] = nb.child[i];
                }
                nb.n--;
                remove(tmp, key);
                return;
            } else if (pos != 0 && x.child[pos - 1].n >= T) {

                divider = x.key[pos - 1];
                nb = x.child[pos - 1];
                x.key[pos - 1] = nb.key[nb.n - 1];
                Node child = nb.child[nb.n];
                nb.n--;

                for (int i = tmp.n; i > 0; i--) {
                    tmp.key[i] = tmp.key[i - 1];
                }
                tmp.key[0] = divider;
                for (int i = tmp.n + 1; i > 0; i--) {
                    tmp.child[i] = tmp.child[i - 1];
                }
                tmp.child[0] = child;
                tmp.n++;
                remove(tmp, key);
                return;
            } else {
                Node lt;
                Node rt;
                boolean last = false;
                if (pos != x.n) {
                    divider = x.key[pos];
                    lt = x.child[pos];
                    rt = x.child[pos + 1];
                } else {
                    divider = x.key[pos - 1];
                    rt = x.child[pos];
                    lt = x.child[pos - 1];
                    last = true;
                    pos--;
                }
                for (int i = pos; i < x.n - 1; i++) {
                    x.key[i] = x.key[i + 1];
                }
                for (int i = pos + 1; i < x.n; i++) {
                    x.child[i] = x.child[i + 1];
                }
                x.n--;
                lt.key[lt.n++] = divider;

                for (int i = 0, j = lt.n; i < rt.n + 1; i++, j++) {
                    if (i < rt.n) {
                        lt.key[j] = rt.key[i];
                    }
                    lt.child[j] = rt.child[i];
                }
                lt.n += rt.n;
                if (x.n == 0) {
                    if (x == root) {
                        root = x.child[0];
                    }
                    x = x.child[0];
                }
                remove(lt, key);
                return;
            }
        }
    }

    public void remove(int key) {
        Node x = binarySearch(root, key);
        if (x == null) {
            return;
        }
        remove(root, key);
    }

    private Node binarySearch(Node x, int key) {
        int i;
        if (x == null)
            return null;

        int start = 0, end = x.n - 1, greater;

        while (true) {
            int pivot = (end + start) / 2;

            if (x.key[pivot] == key) {
                return x;
            }

            greater = x.key[pivot] < key ? 1 : 0;

            if ((end - start) < 1) {
                i = start + greater;
                break;
            }

            if (x.key[pivot] < key) {
                start = pivot + 1;
            } else {
                end = pivot - 1;
            }
        }

        if (x.leaf) {
            return null;
        } else {
            return binarySearch(x.child[i], key);
        }
    }

    public boolean contains(int key) {
        return binarySearch(root, key) != null;
    }

    public List<Integer> traverse() {
        if (this.root != null)
            return this.root.traverse();

        return new ArrayList<>();
    }

    public void save() throws IOException {
        Writer writer = new FileWriter("db.txt");

        traverse().forEach(item -> {
            try {
                writer.write(String.valueOf(item) + ' ');
            } catch (IOException e) {
                e.printStackTrace();
            }
        });

        writer.close();
    }

    public void load(String path) throws FileNotFoundException {
        Scanner scanner = new Scanner(new FileReader(path));

        this.root = new Node();

        Arrays.stream(scanner.nextLine().split("\\s")).forEach(item -> this.insert(Integer.parseInt(item)));
    }

    public static void main(String[] args) {
        BTree b = new BTree(50);

        b.insert(123);
        b.insert(54);
        b.insert(73);
        b.insert(442);
        b.insert(4);
        b.insert(43);
        b.insert(123);
        b.insert(2141);
        b.insert(875);
        b.insert(1823);
        b.insert(896);
        b.insert(97);
        b.insert(92);
        b.insert(9346);
        b.insert(458);
        b.insert(57);
        b.insert(456);
        b.insert(10);

        System.out.println(b.traverse());

        System.out.println(b.contains(100));
        System.out.println(b.contains(442));
        System.out.println(b.contains(456));
        System.out.println(b.contains(9346));
        System.out.println(b.contains(2314));
        System.out.println(b.contains(54));
        System.out.println(b.contains(4));

    }
}