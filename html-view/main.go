package main
//用来批量读取本地html文件提供给前端使用
//用go build main.go 编译成可执行文件提供给前端调用
import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sort"
	"strings"
)

type HTMLFile struct {
	Name string `json:"name"`
	Path string `json:"path"`
}

var (
	currentDir string
)

func main() {
	// 设置静态文件服务
	var err error
	currentDir, err = os.Getwd()
	if err != nil {
		log.Printf("获取当前目录失败: %v", err)
		return
	}
	mux := http.NewServeMux()
	// HTML 文件路由（带特殊头）
	mux.HandleFunc("/html/", htmlFileHandler)
	// 其他静态文件
	mux.Handle("/", http.FileServer(http.Dir(currentDir)))

	// API 路由 - 获取 HTML 文件列表
	mux.HandleFunc("/api/files", getHTMLFiles)

	// 应用安全头中间件
	handler := securityHeaders(mux)

	log.Println("服务器启动在 http://localhost:8089")
	log.Fatal(http.ListenAndServe(":8089", handler))
}

// HTML 文件处理器
func htmlFileHandler(w http.ResponseWriter, r *http.Request) {
	// 设置允许加载外部资源
	w.Header().Set("Content-Security-Policy", "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;")
	w.Header().Set("X-Content-Type-Options", "nosniff")

	// 提供 HTML 文件
	http.FileServer(http.Dir(currentDir)).ServeHTTP(w, r)
}

// CORS 和安全头中间件
func securityHeaders(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// CORS 头
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		// 允许加载外部资源（图片、CSS、JS等）
		w.Header().Set("Content-Security-Policy", "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;")

		// 允许在 iframe 中显示
		w.Header().Set("X-Frame-Options", "ALLOWALL")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}
func getHTMLFiles(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	// HTML 文件目录路径
	htmlDir := fmt.Sprintf("%s/public/resource/html", currentDir)

	// 读取目录
	files, err := os.ReadDir(htmlDir)
	if err != nil {
		http.Error(w, "无法读取目录", http.StatusInternalServerError)
		log.Printf("读取目录错误: %v", err)
		return
	}

	// 过滤并排序 HTML 文件
	var htmlFiles []HTMLFile
	for _, file := range files {
		if !file.IsDir() && strings.HasSuffix(file.Name(), ".html") {
			htmlFiles = append(htmlFiles, HTMLFile{
				Name: strings.TrimSuffix(file.Name(), ".html"),
				Path: "/html/" + file.Name(),
			})
		}
	}

	// 按文件名排序
	sort.Slice(htmlFiles, func(i, j int) bool {
		return htmlFiles[i].Name < htmlFiles[j].Name
	})

	// 返回 JSON
	json.NewEncoder(w).Encode(htmlFiles)
}
