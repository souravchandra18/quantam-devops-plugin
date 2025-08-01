package com.example.user;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
class UserServiceTest {
    @Test void testGetUser() {
        assertEquals("Alice", new UserService().getUser(1));
    }
}
