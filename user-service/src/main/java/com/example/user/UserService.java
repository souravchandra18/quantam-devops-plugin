package com.example.user;
public class UserService {
    public String getUser(int id) {
        return id == 1 ? "Alice" : "Bob";
    }
}
