package com.example.claims;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
class ClaimsServiceTest {
    @Test void testProcessClaim() {
        assertTrue(new ClaimsService().processClaim("CLM123"));
    }
}
