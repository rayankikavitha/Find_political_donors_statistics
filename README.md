# Find_political_donors_statistics


Find_political_donors 

Following program provides running median, count, total sum donated by zipcode. and transaction_date. Works for streaming data.


Required packages: heapq, math, pandas, os, sys, dateutil.parser


Summary:
The Federal Election Commission regularly publishes campaign contributions and while you don’t want to pull specific donors from those files — because using that information for fundraising or commercial purposes is illegal — you want to identify the areas (zip codes) that may be fertile ground for soliciting future donations for similar candidates.
Because those donations may come from specific events (e.g., high-dollar fundraising dinners) but aren’t marked as such in the data, you also want to identify which time periods are particularly lucrative so that an analyst might later correlate them to specific fundraising events.

Input file:

The Federal Election Commission provides data files stretching back years and is regularly updated
For the purposes of this challenge, we’re interested in individual contributions. While you're welcome to run your program using the data files found at the FEC's website, you should not assume that we'll be testing your program on any of those data files or that the lines will be in the same order as what can be found in those files. Our test data files, however, will conform to the data dictionary as described by the FEC.
Also, while there are many fields in the file that may be interesting, below are the ones that you’ll need to complete this challenge:
CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution ZIP_CODE: zip code of the contributor (we only want the first five digits/characters) TRANSACTION_DT: date of the transaction TRANSACTION_AMT: amount of the transaction OTHER_ID: a field that denotes whether contribution came from a person or an entity

Output files

medianvals_by_zip.txt:

contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code The output file medianvals_by_zip.txt should contain the same number of lines or records as the input data file minus any records that were ignored as a result of the 'Input file considerations.'
Each line of this file should contain these fields:
recipient of the contribution (or CMTE_ID from the input file) 5-digit zip code of the contributor (or the first five characters of the ZIP_CODE field from the input file) running median of contributions received by recipient from the contributor's zip code streamed in so far. Median calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar) total number of transactions received by recipient from the contributor's zip code streamed in so far total amount of contributions received by recipient from the contributor's zip code streamed in so far When creating this output file, you can choose to process the input data file line by line, in small batches or all at once depending on which method you believe to be the best given the challenge description. However, when calculating the running median, total number of transactions and total amount of contributions, you should only take into account the input data that has streamed in so far -- in other words, from the top of the input file to the current line. See the below example for more guidance.

medianvals_by_date.txt:

has the calculated median, total dollar amount and total number of contributions by recipient and date.
Each line of this file should contain these fields:
recipeint of the contribution (or CMTE_ID from the input file) date of the contribution (or TRANSACTION_DT from the input file) median of contributions received by recipient on that date. Median calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar) total number of transactions received by recipient on that date total amount of contributions received by recipient on that date This second output file does not depend on the order of the input file, and in fact should be sorted alphabetical by recipient and then chronologically by date.

Example

Suppose your input file contained only the following few lines. Note that the fields we are interested in are in bold below but will not be like that in the input file. There's also an extra new line between records below, but the input file won't have that.
If we were to pick the relevant fields from each line, here is what we would record for each line.
1. 
CMTE_ID: C00629618 ZIP_CODE: 90017 TRANSACTION_DT: 01032017 TRANSACTION_AMT: 40 OTHER_ID: H6CA34245
2. 
CMTE_ID: C00177436 ZIP_CODE: 30004 TRANSACTION_DT: 01312017 TRANSACTION_AMT: 384 OTHER_ID: empty
3. 
CMTE_ID: C00384818 ZIP_CODE: 02895 TRANSACTION_DT: 01122017 TRANSACTION_AMT: 250 OTHER_ID: empty
4. 
CMTE_ID: C0017743 ZIP_CODE: 30750 TRANSACTION_DT: 01312017 TRANSACTION_AMT: 230 OTHER_ID: empty
5. 
CMTE_ID: C00177436 ZIP_CODE: 04105 TRANSACTION_DT: 01312017 TRANSACTION_AMT: 384 OTHER_ID: empty
6. 
CMTE_ID: C00384818 ZIP_CODE: 02895 TRANSACTION_DT: 01122017 TRANSACTION_AMT: 333 OTHER_ID: empty
7. 
CMTE_ID: C00177436 ZIP_CODE: 04105 TRANSACTION_DT: 01312017 TRANSACTION_AMT: 384 OTHER_ID: empty

We would ignore the first record because the OTHER_ID field contains data and is not empty. Moving to the next record, we would write out the first line of medianvals_by_zip.txt to be:

C00177436|30004|384|1|384

Note that because we have only seen one record streaming in for that recipient and zip code, the running median amount of contribution and total amount of contribution is 384.
Looking through the other lines, note that there are only two recipients for all of the records we're interested in our input file (minus the first line that was ignored due to non-null value of OTHER_ID).
Also note that there are two records with the recipient C00177436 and zip code of 04105 totaling $768 in contributions while the recipient C00384818 and zip code 02895 has two contributions totaling $583 (250 + 333) and a median of $292 (583/2 = 291.5 or 292 when rounded up)
Processing all of the input lines, the entire contents of medianvals_by_zip.txt would be:

C00177436|30004|384|1|384
C00384818|02895|250|1|250 
C00177436|30750|230|1|230
C00177436|04105|384|1|384 
C00384818|02895|292|2|583
C00177436|04105|384|2|768

If we drop the zip code, there are four records with the same recipient, C00177436, and date of 01312017. Their total amount of contributions is $1,382.

For the recipient, C00384818, there are two records with the date 01122017 and total contribution of $583 and median of $292.
As a result, medianvals_by_date.txt would contain these lines in this order:

C00177436|01312017|384|4|1382
C00384818|01122017|292|2|583
