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

countMatches:: Eq a => [a] -> Store (Int,Int) a -> Int
countMatches as g = 
    length $ 
    filter id $ 
    [ isMatch as g (\(x,y) -> (x+dx,y+dy)) | 
        dx <- [-1..1], 
        dy <- [-1..1], 
        dx /= 0 || dy /= 0 
    ]

countAllMatches :: Eq a => [a] -> Grid a -> Int 
countAllMatches as (Grid w h m) =
  let 
    gridWithCount = extend (countMatches as) m
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
    let result = countAllMatches "XMAS" grid
    print $ show result


-- 2562