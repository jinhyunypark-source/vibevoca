import 'dart:io';
import 'package:supabase/supabase.dart';
import 'package:csv/csv.dart';

// ⚠️ Configuration: Set these before running
const String supabaseUrl = 'https://anizwbojntonkfwgyosa.supabase.co';
const String supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFuaXp3Ym9qbnRvbmtmd2d5b3NhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzI5ODI3MiwiZXhwIjoyMDgyODc0MjcyfQ.6w88AeTdk3LqusTn21L_JYnIoKy2LqgfmuucTJyyp_k'; // MUST Use Service Role Key for Admin Writes

Future<void> main() async {
  if (supabaseUrl == 'YOUR_SUPABASE_URL') {
    print('❌ Error: Please update supabaseUrl and supabaseKey in the script.');
    return;
  }

  print('🚀 Starting Database Seed...');
  
  final client = SupabaseClient(supabaseUrl, supabaseKey);

  // 1. Read CSV
  final file = File('./sample/merged_vocabulary_v3.csv');
  if (!file.existsSync()) {
    print('❌ Error: CSV file not found at ${file.path}');
    return;
  }
  
  final input = file.readAsStringSync();
  // Using simple split for this specific CSV structure since we know it's consistent
  // Or better, use csv package if available. Assuming csv package is added.
  final rows = const CsvToListConverter().convert(input, eol: '\n');

  // Skip header row
  final dataRows = rows.skip(1).toList();
  print('📊 Found ${dataRows.length} words to process.');

  // Cache for avoiding duplicates during this run
  final Map<String, String> categoryIdMap = {}; // Title -> UUID
  final Map<String, String> deckIdMap = {};     // Title -> UUID

  int successCount = 0;

  for (final row in dataRows) {
    if (row.length < 6) continue;

    // Columns: English(0), Definition(1), Ex1(2), Ex2(3), Category(4), DeckGroup(5)
    final word = row[0].toString().trim();
    final definition = row[1].toString().trim();
    final ex1 = row[2].toString().trim();
    final ex2 = row[3].toString().trim();
    final categoryTitle = row[4].toString().trim();
    final deckTitle = row[5].toString().trim();

    // 2. Ensure Category Exists
    String? catId = categoryIdMap[categoryTitle];
    if (catId == null) {
      // Check DB or Insert
      final existing = await client.from('categories').select('id').eq('title', categoryTitle).maybeSingle();
      if (existing != null) {
        catId = existing['id'] as String;
      } else {
        final res = await client.from('categories').insert({'title': categoryTitle}).select();
        catId = res[0]['id'] as String;
        print('Created Category: $categoryTitle');
      }
      categoryIdMap[categoryTitle] = catId!;
    }

    // 3. Ensure Deck Exists
    // Unique Deck Key: CategoryID + DeckTitle (Since logic_clarity might appear in diff categories? unlikely but safe)
    final deckKey = '${catId}_$deckTitle';
    String? deckId = deckIdMap[deckKey];
    if (deckId == null) {
       // Assign color based on title logic
       String color = '#FF5733'; // Default Red-Orange
       final titleUpper = deckTitle.toUpperCase();
       if (titleUpper.contains('LOGIC')) color = '#3498DB'; 
       else if (titleUpper.contains('EMOTION')) color = '#9B59B6';
       else if (titleUpper.contains('SENSORY')) color = '#F1C40F';
       else if (titleUpper.contains('ACTION')) color = '#E74C3C';
       else if (titleUpper.contains('SOCIAL')) color = '#2ECC71';
       else if (titleUpper.contains('BUSINESS')) color = '#34495E';
       else if (titleUpper.contains('ACADEMIC')) color = '#1ABC9C';
       else if (titleUpper.contains('DAILY')) color = '#E67E22';
       else if (titleUpper.contains('TRAVEL')) color = '#16A085';
       else if (titleUpper.contains('ART')) color = '#D35400';
       else if (titleUpper.contains('NATURE')) color = '#27AE60';
       else if (titleUpper.contains('TECH')) color = '#7F8C8D';
       else if (titleUpper.contains('HEALTH')) color = '#F39C12';
       else if (titleUpper.contains('FOOD')) color = '#C0392B';
       else if (titleUpper.contains('TIME')) color = '#8E44AD';

       // Check if exists
       final existing = await client.from('decks').select('id').eq('title', deckTitle).eq('category_id', catId).maybeSingle();

       if (existing != null) {
         // Update existing deck color
         await client.from('decks').update({
           'color': color,
         }).eq('id', existing['id']);
         deckId = existing['id'] as String;
         // print('Updated Deck Color: $deckTitle');
       } else {
         // Insert new deck
         final res = await client.from('decks').insert({
           'title': deckTitle,
           'category_id': catId,
           'icon': '📝',
           'color': color,
         }).select();
         deckId = res[0]['id'] as String;
         print('Created Deck: $deckTitle');
       }
       
       deckIdMap[deckKey] = deckId!;
    }

    // 4. Insert Card
    try {
      await client.from('cards').insert({
        'deck_id': deckId,
        'front_text': word,
        'back_text': definition,
        'example_sentences': [ex1, ex2].where((e) => e.isNotEmpty).toList(),
      });
      successCount++;
      if (successCount % 50 == 0) stdout.write('.');
    } catch (e) {
      print('❌ Failed to insert $word: $e');
    }
  }

  print('\n✅ Import Completed! Inserted $successCount words.');
}
