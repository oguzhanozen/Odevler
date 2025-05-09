-- Veritabaný Oluþturma
CREATE DATABASE GameManagement;
GO

USE GameManagement;
GO
-- Oyuncular tablosunu oluþturur
CREATE TABLE Players (
    PlayerID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(50) NOT NULL,
    DateJoined DATE NOT NULL
);

-- Oyunlar tablosunu oluþturur
CREATE TABLE Games (
    GameID INT PRIMARY KEY IDENTITY(1,1),
    GameName VARCHAR(100) NOT NULL,
    Genre VARCHAR(50) NOT NULL
);

-- Sonuçlar tablosunu oluþturur
CREATE TABLE Scores (
    ScoreID INT PRIMARY KEY IDENTITY(1,1),
    PlayerID INT NOT NULL,
    GameID INT NOT NULL,
    Score INT NOT NULL,
    DatePlayed DATE NOT NULL,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (GameID) REFERENCES Games(GameID)
);

-- Arkadaþlýklar tablosunu oluþturur
CREATE TABLE Friendships (
    FriendshipID INT PRIMARY KEY IDENTITY(1,1),
    PlayerID1 INT NOT NULL,
    PlayerID2 INT NOT NULL,
    DateAdded DATE NOT NULL,
    FOREIGN KEY (PlayerID1) REFERENCES Players(PlayerID),
    FOREIGN KEY (PlayerID2) REFERENCES Players(PlayerID)
);

-- Yorumlar tablosunu oluþturur
CREATE TABLE Comments (
    CommentID INT PRIMARY KEY IDENTITY(1,1),
    PlayerID INT NOT NULL,
    GameID INT NOT NULL,
    CommentText TEXT NOT NULL,
    DatePosted DATE NOT NULL,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (GameID) REFERENCES Games(GameID)
);

