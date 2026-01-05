import zemberek.morphology.TurkishMorphology;
import zemberek.normalization.TurkishSpellChecker;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Scanner;

public class ZemberekSpellChecker {

    public static void main(String[] args) throws IOException {
        // Zemberek başlatılıyor
        TurkishMorphology morphology = TurkishMorphology.createWithDefaults();
        TurkishSpellChecker spellChecker = new TurkishSpellChecker(morphology);

        // Kullanıcıdan cümle al
        Scanner scanner = new Scanner(System.in);
        System.out.print("Lütfen bir cümle girin: ");
        String input = scanner.nextLine();
        scanner.close();

        String[] words = input.split("\\s+");

        FileWriter writer = new FileWriter("oneriler.txt", java.nio.charset.StandardCharsets.UTF_8);
        for (String word : words) {
            if (!spellChecker.check(word)) {
                List<String> suggestions = spellChecker.suggestForWord(word);
                if (!suggestions.isEmpty()) {
                    writer.write(word + ":" + String.join(",", suggestions) + "\n");
                }
            }
        }
        writer.close();


        System.out.println("Öneriler dosyaya yazıldı.");
    }
}
