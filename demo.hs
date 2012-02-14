module Main where

main = do putStr "What is your name? "
          name <- read
          putStrLn ("Hello, " ++ name)
