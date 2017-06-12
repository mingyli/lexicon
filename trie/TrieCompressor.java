import java.util.List;
import java.util.Scanner;
import java.io.File;
import java.io.PrintWriter;
import java.io.FileNotFoundException;

/**
 * TrieCompressor uses a trie to determine
 * unique points of words. It is good
 * for compressing text with many 
 * long words.
 *
 * This usually performs very poorly.
 *
 *
 * How to use this utility:
 *
 * {@code java TrieCompressor <input_file> <output_file>}
 *
 * @author Ming Li
 *
 */

public class TrieCompressor {
    private Trie trie;
    private String inputFile;

    /**
     * The constructor takes text from a file
     * and forms a trie with words from the text.
     * @param inputFile the name of the file
     */
    public TrieCompressor(String inputFile) {
        trie = new Trie();
        this.inputFile = inputFile;
        
        try {
            Scanner scanner = new Scanner(new File(inputFile));
            while (scanner.hasNext()) {
                String word = scanner.next();
                trie.insert(word);
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.err.println(inputFile + " not found.");
        }
    }

    /**
     * This method writes the compressed contents of `inputFile`
     * to `outputFile`.
     * @param outputFile the name of the output file
     */
    private void compressToFile(String outputFile) {
        try {
            Scanner scanner = new Scanner(new File(inputFile));
            // String[] tokens = fileName.split("\\.(?=[^\\.]+$)");
            // PrintWriter output = new PrintWriter(tokens[0] + ".trie");
            PrintWriter output = new PrintWriter(outputFile);
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                // String[] words = line.split("((?<=\\s+)|(?=\\s+))");
                String[] words = line.split("\\b");
                for (String word : words) {
                    String compressed = compress(word);
                    output.print(compressed);
                }
                output.println();
            }
            scanner.close();
            output.close();
        } catch (FileNotFoundException e) {
            System.err.println(outputFile + " not found.");
        }
    }


    private String compress(String s) {
        // assert s in lexicon
        for (int i = 0; i < s.length(); i++) {
            String prefix = s.substring(0, i);
            List<String> completed = trie.getByPrefix(prefix);
            if (completed.size() == 1) {
                return prefix;
            }
        }
        return s;
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            throw new IllegalArgumentException("provide <input_file> and <output_file>");
        }
        TrieCompressor tc = new TrieCompressor(args[0]);
        tc.compressToFile(args[1]);


        // String[] lexicon = {"vanguard", "comatose", "vantage"};
        // tc = new TrieCompressor(lexicon);
        // System.out.println(tc.compress("vanguard"));
        // System.out.println(tc.compress("comatose"));
        // System.out.println(tc.compress("vantage"));

        // tc = new TrieCompressor("text.txt");
        // System.out.println(tc.compress("cardboard"));
        // System.out.println(tc.compress("language"));
        // System.out.println(tc.compress("berkeley"));
        // System.out.println(tc.compress("processing"));
        // System.out.println(tc.compress("computer"));
    }
}
