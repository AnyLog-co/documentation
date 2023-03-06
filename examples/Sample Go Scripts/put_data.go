package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "math/rand"
    "net/http"
    "time"
)

func put_data(conn string, dbms string, tale string, mode string, payload map) {
     var url string = fmt.Sprintf("http://%s", conn)

    mappingBytes, err := json.Marshal(payload)
    if err != nil {
        fmt.Println("Fail to convert payload (Error: %s)", err)
        return
    }

    req, err := http.NewRequest("PUT", url, bytes.NewBuffer(mappingBytes))
    if err != nil {
        fmt.Println("Failed to prepare error against %s (Error: %s)", conn, err)
        return
    }

    client := &http.Client{}

    req.Header.Add("type", "json")
    req.Header.Add("dbms", dbms)
    req.Header.Add("table", table)
    if mode == "streaming" || mode == "file" {
       req.Header.Add("mode", mode)
    } else {
       req.Header.Add("mode", "streaming")
    }
   req.Header.Add("Content-Type", "text/plain")

    resp, err := client.Do(req)
    if err != nil {
        fmt.Println("Failed to execute PUT against %s (Error: %s)", conn, err)
        return
    } else {
        defer resp.Body.Close()
        fmt.Println("Response status:", resp.Status)
    }

}

func main() {
    var conn string  = "127.0.0.1:32149"
    var dbms string  = "test"
    var table string = "sample_data"
    var mode string  = "streaming"

    payload := map[string]interface{}{
        "timestamp": time.Now().Format("2006-01-02 15:04:05"),
        "value": rand.Intn(100),
        "unit": "Celsius"}

    put_data(conn: conn, dbms: dbms, tale: table, mode: mode, payload)
}



