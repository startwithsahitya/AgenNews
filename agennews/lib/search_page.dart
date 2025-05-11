import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({Key? key}) : super(key: key);

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  List<dynamic> _allNews = [];
  List<dynamic> _filteredNews = [];
  bool _isLoading = true;
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _loadNews();
  }

  Future<void> _loadNews() async {
    final String response =
        await rootBundle.loadString('assets/data/news_data.json');
    final data = await json.decode(response);
    setState(() {
      _allNews = data;
      _filteredNews = data;
      _isLoading = false;
    });
  }

  void _filterNews(String query) {
    setState(() {
      _searchQuery = query;
      if (query.isEmpty) {
        _filteredNews = _allNews;
      } else {
        _filteredNews = _allNews.where((news) {
          final genre = news['genre'].toString().toLowerCase();
          final title = news['title'].toString().toLowerCase();
          final description = news['description'].toString().toLowerCase();
          final source = news['source'].toString().toLowerCase();
          final q = query.toLowerCase();
          return genre.contains(q) ||
              title.contains(q) ||
              description.contains(q) ||
              source.contains(q);
        }).toList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Search by genre, topic, or keyword...',
              prefixIcon: const Icon(Icons.search),
              border:
                  OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onChanged: _filterNews,
          ),
        ),
        Expanded(
          child: _filteredNews.isEmpty
              ? const Center(child: Text('No news found.'))
              : ListView.builder(
                  itemCount: _filteredNews.length,
                  itemBuilder: (context, index) {
                    final news = _filteredNews[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      child: ListTile(
                        leading: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(
                            news['image'],
                            width: 60,
                            height: 60,
                            fit: BoxFit.cover,
                          ),
                        ),
                        title: Text(news['title'],
                            maxLines: 2, overflow: TextOverflow.ellipsis),
                        subtitle: Text(news['genre']),
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }
}
