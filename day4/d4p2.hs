module Main where

import Control.Comonad
import Control.Comonad.Store

data Grid a = Grid {
    gwidth :: Int,
    gheight :: Int,
    gdata :: Store (Int,Int) a
}

isMatch :: Eq a => [a] -> Store i a -> (i -> i) -> Bool
isMatch as g step = 
  let 
    positions = iterate step (pos g)
    matches = map (\(a,i) -> peek i g == a) (zip as positions)
  in 
    all id matches

isMatch2 :: Store (Int,Int) Char -> Bool
isMatch2 g = 
    let
        (cx,cy) = pos g
        c = peek (cx,cy) g
        ul = peek (cx-1,cy-1) g
        ur = peek (cx+1,cy-1) g
        ll = peek (cx-1,cy+1) g
        lr = peek (cx+1,cy+1) g
    in
        c == 'A' &&
        (ul == 'M' && lr == 'S' || ul == 'S' && lr == 'M') &&
        (ur == 'M' && ll == 'S' || ur == 'S' && ll == 'M')

countMatches:: Store (Int,Int) Char -> Int
countMatches g = if isMatch2 g then 1 else 0

countAllMatches :: Grid Char -> Int 
countAllMatches (Grid w h m) =
  let 
    gridWithCount = extend countMatches m
    enumerateGrid = [(x, y) | x <- [0 .. w - 1], y <- [0 .. h - 1]]
  in 
    sum $ map (\i -> peek i gridWithCount) enumerateGrid

mkGrid :: [String] -> Grid Char
mkGrid matrix = Grid width height (store accessor (0,0))
  where 
    height = length $ matrix
    width = length $ matrix !! 0
    accessor :: (Int,Int) -> Char
    accessor (x,y) = 
        if x >= 0 && x < width && y >= 0 && y < height then
            (matrix !! y) !! x
        else
            '.'

main :: IO ()
main = do
    content <- readFile "app/input.txt"
    let linesOfFile = lines content 
    let grid = mkGrid linesOfFile
    let result = countAllMatches grid
    print $ show result


-- 2562