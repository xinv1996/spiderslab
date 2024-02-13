package main

import (
	"context"
	"encoding/json"
	"fmt"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"io"
	"log"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

const (
	proxyURL = "http://127.0.0.1:2333"
	mongoURL = "mongodb://233.233.233.233:2333"
)

type blogInfo struct {
	UserID       string    `json:"userId" bson:"userId"`
	Title        string    `json:"title" bson:"title"`
	CommentCount float64   `json:"commentCount" bson:"commentCount"`
	LikeCount    float64   `json:"likeCount" bson:"likeCount"`
	Shortcode    string    `json:"shortcode" bson:"shortcode"`
	PublishTime  time.Time `json:"publishTime" bson:"publishTime"`
	CreateTime   time.Time `json:"createTime" bson:"createTime"`
}

type UserProfile struct {
	UserID     string    `json:"userId" bson:"userId"`
	UserName   string    `json:"userName" bson:"userName"`
	Followers  float64   `json:"followers" bson:"followers"`
	Biography  string    `json:"biography" bson:"biography"`
	Follow     float64   `json:"follow" bson:"follow"`
	Blog       float64   `json:"blog" bson:"blog"`
	CreateTime time.Time `json:"createTime" bson:"createTime"`
}

func crawlBlogInfo(userId string, endCursor string, mgClient *mongo.Client) (bool, string, error) {
	proxyURL, err := url.Parse(proxyURL)
	if err != nil {
		fmt.Println("Error parsing proxy URL:", err)
		return false, "", err
	}
	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
	}
	client := &http.Client{
		Transport: transport,
	}
	params := `%7B"id"%3A"` + userId + `"%2C"after"%3A"` + endCursor + `"%2C"first"%3A12%7D`
	urlStr := fmt.Sprintf("https://www.instagram.com/graphql/query/?doc_id=%s&variables=%s", "自定义doc_id", params)
	req, err := http.NewRequest("GET", urlStr, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return false, "", err
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
	req.Header.Set("x-ig-app-id", "app_id")
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error fetching the page:", err)
		return false, "", err
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)

	if err != nil {
		fmt.Println("Error reading response body:", err)
		return false, "", err
	}
	var jsonData map[string]interface{}
	err = json.Unmarshal(body, &jsonData)
	if err != nil {
		fmt.Println("Error parsing JSON:", err)
		return false, "", err
	}
	var rootPath []interface{}
	if data, ok := jsonData["data"].(map[string]interface{}); ok {
		if user, ok := data["user"].(map[string]interface{}); ok {
			if edgeOwnerToTimelineMedia, ok := user["edge_owner_to_timeline_media"].(map[string]interface{}); ok {
				if edges, ok := edgeOwnerToTimelineMedia["edges"].([]interface{}); ok {
					rootPath = edges
				}
			}
		}
	}
	if rootPath == nil {
		fmt.Println("Unexpected JSON structure")
		return false, "", nil
	}
	for _, item := range rootPath {
		titleNode := item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_to_caption"].(map[string]interface{})["edges"].([]interface{})
		var title string
		if len(titleNode) == 0 {
			log.Println("title : No data available in edges")
		} else {
			title = item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_to_caption"].(map[string]interface{})["edges"].([]interface{})[0].(map[string]interface{})["node"].(map[string]interface{})["text"].(string)
		}
		if title != "" {
			commentCount := item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_to_comment"].(map[string]interface{})["count"].(float64)
			likeCount := item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_preview_like"].(map[string]interface{})["count"].(float64)
			shortcode := item.(map[string]interface{})["node"].(map[string]interface{})["shortcode"].(string)
			tm := item.(map[string]interface{})["node"].(map[string]interface{})["taken_at_timestamp"].(float64)
			timestamp := time.Unix(int64(tm), 0)
			insBlogInfo := mgClient.Database("crawlers").Collection("ins_blog_info_v1")
			insBlogItem := blogInfo{
				UserID:       userId,
				Title:        title,
				CommentCount: commentCount,
				LikeCount:    likeCount,
				Shortcode:    shortcode,
				PublishTime:  timestamp,
				CreateTime:   time.Now(),
			}
			insertOneRes, insertErr := insBlogInfo.InsertOne(context.TODO(), insBlogItem)
			if insertErr != nil {
				insertFlag := strings.Index(insertErr.Error(), "[E11000 duplicate key error collection")
				if insertFlag != -1 {
					fmt.Println("DATA REPEAT!!!")
					continue
				} else {
					fmt.Println("CODE ERROR!!!")
					fmt.Println(insertErr.Error())
					continue
				}
			} else {
				fmt.Printf("写入成功:%v\n", insertOneRes.InsertedID)
			}
		} else {
			fmt.Println("title is empty")
			continue
		}
	}
	hasNextPage := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["page_info"].(map[string]interface{})["has_next_page"].(bool)
	endCursorNext := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["page_info"].(map[string]interface{})["end_cursor"].(string)
	return hasNextPage, endCursorNext, nil
}

func crawlUserProfile(wg *sync.WaitGroup, urlStr string, mgClient *mongo.Client) {
	defer wg.Done()
	proxyURL, err := url.Parse(proxyURL)
	if err != nil {
		fmt.Println("Error parsing proxy URL:", err)
		return
	}
	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
	}
	client := &http.Client{
		Transport: transport,
	}
	req, err := http.NewRequest("GET", urlStr, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
	req.Header.Set("x-ig-app-id", "自定义app_id")
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error fetching the page:", err)
		return
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return
	}

	var jsonData map[string]interface{}
	err = json.Unmarshal(body, &jsonData)
	if err != nil {
		fmt.Println("Error parsing JSON:", err)
		return
	}

	var biography string = jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["biography"].(string)
	followers := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_followed_by"].(map[string]interface{})["count"].(float64)
	fllow := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_follow"].(map[string]interface{})["count"].(float64)
	blog := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["count"].(float64)
	userName := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["edges"].([]interface{})[0].(map[string]interface{})["node"].(map[string]interface{})["owner"].(map[string]interface{})["username"].(string)
	userId := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["edges"].([]interface{})[0].(map[string]interface{})["node"].(map[string]interface{})["owner"].(map[string]interface{})["id"].(string)
	insUserProfile := mgClient.Database("crawlers").Collection("ins_user_profile")
	insUserItem := UserProfile{
		UserID:     userId,
		UserName:   userName,
		Followers:  followers,
		Biography:  biography,
		Follow:     fllow,
		Blog:       blog,
		CreateTime: time.Now(),
	}
	fmt.Println(insUserItem)
	insertOneRes, insertErr := insUserProfile.InsertOne(context.TODO(), insUserItem)
	if insertErr != nil {
		insertFlag := strings.Index(insertErr.Error(), "[E11000 duplicate key error collection")
		if insertFlag != -1 {
			fmt.Println("DATA REPEAT!!!")
		} else {
			fmt.Println("CODE ERROR!!!")
			fmt.Println(insertErr.Error())
		}
	} else {
		fmt.Printf("写入成功:%v\n", insertOneRes.InsertedID)
	}

	rootPath := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["edges"].([]interface{})
	for _, item := range rootPath {
		titleNode := item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_to_caption"].(map[string]interface{})["edges"].([]interface{})
		var title string
		if len(titleNode) == 0 {
			log.Println("title : No data available in edges")
		} else {
			title = item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_to_caption"].(map[string]interface{})["edges"].([]interface{})[0].(map[string]interface{})["node"].(map[string]interface{})["text"].(string)
		}

		commentCount := item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_to_comment"].(map[string]interface{})["count"].(float64)
		likeCount := item.(map[string]interface{})["node"].(map[string]interface{})["edge_media_preview_like"].(map[string]interface{})["count"].(float64)
		shortcode := item.(map[string]interface{})["node"].(map[string]interface{})["shortcode"].(string)
		tm := item.(map[string]interface{})["node"].(map[string]interface{})["taken_at_timestamp"].(float64)
		timestamp := time.Unix(int64(tm), 0)
		insBlogInfo := mgClient.Database("crawlers").Collection("ins_blog_info")
		insBlogItem := blogInfo{
			UserID:       userId,
			Title:        title,
			CommentCount: commentCount,
			LikeCount:    likeCount,
			Shortcode:    shortcode,
			PublishTime:  timestamp,
			CreateTime:   time.Now(),
		}
		insertOneRes, insertErr := insBlogInfo.InsertOne(context.TODO(), insBlogItem)
		if insertErr != nil {
			insertFlag := strings.Index(insertErr.Error(), "[E11000 duplicate key error collection")
			if insertFlag != -1 {
				fmt.Println("DATA REPEAT!!!")
			} else {
				fmt.Println("CODE ERROR!!!")
				fmt.Println(insertErr.Error())
			}
		} else {
			fmt.Printf("写入成功:%v\n", insertOneRes.InsertedID)
		}

	}
	hasNextPage := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["page_info"].(map[string]interface{})["has_next_page"].(bool)
	endCursor := jsonData["data"].(map[string]interface{})["user"].(map[string]interface{})["edge_owner_to_timeline_media"].(map[string]interface{})["page_info"].(map[string]interface{})["end_cursor"].(string)

	for hasNextPage {
		hasNextPage, endCursor, err = crawlBlogInfo(userId, endCursor, mgClient)
		if err != nil {
			fmt.Println("Error fetching the page:", err)

		} else {
			fmt.Println("NextPage:", endCursor)
		}
	}

}

func main() {
	clientOptions := options.Client().ApplyURI(mongoURL)
	mgClient, cllectErr := mongo.Connect(context.TODO(), clientOptions)
	if cllectErr != nil {
		log.Fatal(cllectErr)
	}
	pingErr := mgClient.Ping(context.TODO(), nil)
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	urls := []string{
		"https://www.instagram.com/api/v1/users/web_profile_info/?username=visit_nanchang",
	}
	var wg sync.WaitGroup

	for _, url := range urls {
		wg.Add(1)
		go crawlUserProfile(&wg, url, mgClient)
	}

	wg.Wait() // 等待所有goroutine完成
	fmt.Println("所有请求完成")
}


