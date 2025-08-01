package com.example.claims;
public class ClaimsService {
    public boolean processClaim(String id) {
        return id != null && id.length() > 3;
    }
}
