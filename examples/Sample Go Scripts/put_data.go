package main

import (
    "flag"
//     "bytes"
//     "encoding/json"
    "fmt"
    "os"
    "regexp"
//     "math/rand"
//     "net/http"
//     "time"
)


func __validate_conn(conn string) bool {
    var status bool = true
    match, _ := regexp.MatchString(`^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$`, conn)
    if !  match {
        status = false
    }

    return status
}

func __validate_mode(mode string) bool {
    var status bool = true
    modeValue := []string{"file", "streaming"}

    for _, modeValue := range modeValue {
        if mode != modeValue {
            status = false
        }
    }

    return status
}


func put_data(conn string) {
     var url string = "http://" + conn
     fmt.Println(url)
}


func main(){
    /**
    :command-line:
        -conn   string      REST connection IP and Port (example IP:Port)
        -db     string      logical database to store data in (default "test")
        -mode   string      store data one at a time or streaming (default "streaming")
        -table  string      table to store data in (default "sample_data")
    :params:
        status:bool - status used to validate mode values
        modeValues:list - list of mode options
    */
    var conn string
    var db_name string
    var table_name string
    var mode string

    flag.StringVar(&conn, "conn", "", "REST connection IP and Port (example IP:Port)")

    flag.StringVar(&db_name, "db", "test", "logical database to store data in")
    flag.StringVar(&table_name, "table", "sample_data", "table to store data in")
    flag.StringVar(&mode, "mode", "streaming", "store data one at a time or streaming")
    flag.Parse()


    if __validate_conn(conn) == false {
        fmt.Println("Invalid format for conn info - expected format 127.0.0.1:3306")
        os.Exit(0)
    }

//     if __validate_mode(mode) == false {
//         fmt.Println("Invalid value for mode. Accepted Values: ", mode)
//         os.Exit(0)
//     }

    put_data(conn)
}

// func put_data(conn string, dbms string, tale string, mode string, payload map) {
//      var url string = fmt.Sprintf("http://%s", conn)
//
//     mappingBytes, err := json.Marshal(payload)
//     if err != nil {
//         fmt.Println("Fail to convert payload (Error: %s)", err)
//         return
//     }
//
//     req, err := http.NewRequest("PUT", url, bytes.NewBuffer(mappingBytes))
//     if err != nil {
//         fmt.Println("Failed to prepare error against %s (Error: %s)", conn, err)
//         return
//     }
//
//     client := &http.Client{}
//
//     req.Header.Add("type", "json")
//     req.Header.Add("dbms", dbms)
//     req.Header.Add("table", table)
//     if mode == "streaming" || mode == "file" {
//        req.Header.Add("mode", mode)
//     } else {
//        req.Header.Add("mode", "streaming")
//     }
//    req.Header.Add("Content-Type", "text/plain")
//
//     resp, err := client.Do(req)
//     if err != nil {
//         fmt.Println("Failed to execute PUT against %s (Error: %s)", conn, err)
//         return
//     } else {
//         defer resp.Body.Close()
//         fmt.Println("Response status:", resp.Status)
//     }
//
// }
//
// func main() {
//     var conn string  = "127.0.0.1:32149"
//     var dbms string  = "test"
//     var table string = "sample_data"
//     var mode string  = "streaming"
//
//     payload := map[string]interface{}{
//         "timestamp": time.Now().Format("2006-01-02 15:04:05"),
//         "value": rand.Intn(100),
//         "unit": "Celsius"}
//
//     put_data(conn: conn, dbms: dbms, tale: table, mode: mode, payload: payload)
// }
//
//
