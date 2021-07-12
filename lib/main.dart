import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_phoenix/flutter_phoenix.dart';
import 'dart:convert';
import 'dart:async';

void main() {
  runApp(
    Phoenix(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tableau de bord Divia',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
      ),
      home: MyHomePage(title: 'Tableau de bord Divia'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  {{ GET_DATA }}


  @override
  Widget build(BuildContext context) {

    refreshLoop(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: SingleChildScrollView(
        child: Column(
          children: [

            {{ INSERT_WIDGETS }}

            Text("\n\n"),
          ],
        ),
        ),
      ),
    floatingActionButton: FloatingActionButton(
      onPressed: () => restartApp(context),
      child: const Icon(Icons.refresh),
    ),
    );
  }
}

Future<List<String>> totem(String lineId, String stopCode) async {
  final response = await http.get(
      Uri.parse("{{ SERVER_ADDRESS }}divia?line_id=$lineId&stop_code=$stopCode"));
  final responseBodyDecoded = jsonDecode(response.body);

  List<String> toReturn = [];

  responseBodyDecoded.forEach((time) => {
    if (int.parse(time) < 1) {
      toReturn.add("À l’approche")
    } else {
      toReturn.add(time + " min")
    }
  });

  if (toReturn.length == 0) {
    toReturn = ["-", "-"];
  } else if (toReturn.length == 1) {
    toReturn.add("-");
  }

  if (response.statusCode == 200) {
    return toReturn;
  } else {
    throw Exception(response.statusCode.toString());
  }
}

restartApp(BuildContext context) {
  Phoenix.rebirth(context);
}

refreshLoop(BuildContext context) async {
  Timer.periodic(Duration(seconds: 15), (Timer t) => restartApp(context));
}
