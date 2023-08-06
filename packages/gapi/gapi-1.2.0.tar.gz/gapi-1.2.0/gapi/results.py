#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague" 

import sys
import codecs
import datetime
import time
import os
import re
from tweet_parser.tweet import Tweet
from gapi.api import *
from simple_n_grams.simple_n_grams import SimpleNGrams

if sys.version_info[0] < 3:
    try:
        reload(sys)
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
        sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    except NameError:
        pass

#############################################
# Some constants to configure column retrieval from TwacsCSV
DATE_INDEX = 1
TEXT_INDEX = 2
LINKS_INDEX = 3
USER_NAME_INDEX = 7 
USER_ID_INDEX = 8
OUTPUT_PAGE_WIDTH = 120 
BIG_COLUMN_WIDTH = 32

class Results():
    """Class for aggregating and accessing search result sets and
       subsets.  Returns derived values for the query specified."""

    def __init__(self
            , user
            , password
            , stream_url
            , paged = False
            , output_file_path = None
            , pt_filter = None
            , max_results = 100
            , start = None
            , end = None
            , count_bucket = None
            , show_query = False
            , hard_max = None
            ):
        """Create a result set by passing all of the require parameters 
           for a query. The Results class runs an API query once when 
           initialized. This allows one to make multiple calls 
           to analytics methods on a single query.
        """
        # run the query
        self.query = Query(user, password, stream_url, paged, output_file_path, hard_max)
        self.query.execute(
            pt_filter=pt_filter
            , max_results = max_results
            , start = start
            , end = end
            , count_bucket = count_bucket
            , show_query = show_query
            )
        self.freq = None

    def get_raw_results(self):
        """Generator of query results"""
        for x in self.query.get_raw_results():
            yield x

    def get_activities(self):
        """Generator of query tweet results."""
        for x in self.query.get_activity_set():
            yield x
    
    def get_time_series(self):
        """Generator of time series for query results."""
        for x in self.query.get_time_series():
            yield x

    def get_top_links(self, n=20):
        """Returns the links most shared in the data set retrieved in
           the order of how many times each was shared."""
        self.freq = SimpleNGrams(char_upper_cutoff=100, tokenizer="space")
        for x in self.query.get_activity_set():
            for link_str in x.most_unrolled_urls:
                self.freq.add(link_str)
        return self.freq.get_tokens(n)
        
    def get_top_users(self, n=50):
        """Returns the users  tweeting the most in the data set retrieved
           in the data set. Users are returned in descending order of how
           many times they were tweeted."""
        self.freq = SimpleNGrams(char_upper_cutoff=20, tokenizer="twitter")
        for x in self.query.get_activity_set():
            self.freq.add(x.screen_name)
        return self.freq.get_tokens(n) 

    def get_users(self, n=None):
        """Returns the user ids for the tweets collected"""
        uniq_users = set()
        for x in self.query.get_activity_set():
            uniq_users.add(x.user_id)
        return uniq_users

    def get_top_grams(self, n=20):
        self.freq = SimpleNGrams(char_upper_cutoff=20, tokenizer="twitter")
        self.freq.sl.add_session_stop_list(["http", "https", "amp", "htt"])
        for x in self.query.get_activity_set():
            self.freq.add(x.all_text)
        return self.freq.get_tokens(n) 
            
    def get_geo(self):
        for x in self.query.get_activity_set():
            if x.geo_coordinates is not None:
                lat_lon = x.geo_coordinates
                activity = {"id": x.id,
                            "postedTime": x.created_at_string.strip(".000Z"),
                            "latitude": lat_lon["latitude"],
                            "longitude": lat_lon["longitude"]
                            }
                yield activity
 
    def get_frequency_items(self, size = 20):
        """Retrieve the token list structure from the last query"""
        if self.freq is None:
            raise VallueError("No frequency available for use case")
        return self.freq.get_tokens(size)

    def __len__(self):
        return len(self.query)

    def __repr__(self):
        if self.last_query_params["count_bucket"] is None:
            res = [u"-"*OUTPUT_PAGE_WIDTH]
            rate = self.query.get_rate()
            unit = "Tweets/Minute"
            if rate < 0.01:
                rate *= 60.
                unit = "Tweets/Hour"
            res.append("     PowerTrack Rule: \"%s\""%self.last_query_params["pt_filter"])
            res.append("  Oldest Tweet (UTC): %s"%str(self.query.oldest_t))
            res.append("  Newest Tweet (UTC): %s"%str(self.query.newest_t))
            res.append("           Now (UTC): %s"%str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
            res.append("        %5d Tweets: %6.3f %s"%(self.query.res_cnt, rate, unit))
            res.append("-"*OUTPUT_PAGE_WIDTH)
            #
            self.query.get_top_users()
            fmt_str = u"%{}s -- %10s     %8s (%d)".format(BIG_COLUMN_WIDTH)
            res.append(fmt_str%( "users", "tweets", "activities", self.res_cnt))
            res.append("-"*OUTPUT_PAGE_WIDTH)
            fmt_str =  u"%{}s -- %4d  %5.2f%% %4d  %5.2f%%".format(BIG_COLUMN_WIDTH)
            for x in self.freq.get_tokens(20):
                res.append(fmt_str%(x[4], x[0], x[1]*100., x[2], x[3]*100.))
            res.append("-"*OUTPUT_PAGE_WIDTH)
            #
            self.query.get_top_links()
            fmt_str = u"%{}s -- %10s     %8s (%d)".format(int(2.5*BIG_COLUMN_WIDTH))
            res.append(fmt_str%( "links", "mentions", "activities", self.res_cnt))
            res.append("-"*OUTPUT_PAGE_WIDTH)
            fmt_str =  u"%{}s -- %4d  %5.2f%% %4d  %5.2f%%".format(int(2.5*BIG_COLUMN_WIDTH))
            for x in self.freq.get_tokens(20):
                res.append(fmt_str%(x[4], x[0], x[1]*100., x[2], x[3]*100.))
            res.append("-"*OUTPUT_PAGE_WIDTH)
            #
            self.query.get_top_grams()
            fmt_str = u"%{}s -- %10s     %8s (%d)".format(BIG_COLUMN_WIDTH)
            res.append(fmt_str%( "terms", "mentions", "activities", self.res_cnt))
            res.append("-"*OUTPUT_PAGE_WIDTH)
            fmt_str =u"%{}s -- %4d  %5.2f%% %4d  %6.2f%%".format(BIG_COLUMN_WIDTH)
            for x in self.freq.get_tokens(20):
                res.append(fmt_str%(x[4], x[0], x[1]*100., x[2], x[3]*100.))
            res.append("-"*OUTPUT_PAGE_WIDTH)
        else:
            res = ["{:%Y-%m-%dT%H:%M:%S},{}".format(x[2], x[1])
                        for x in self.get_time_series()]
        return u"\n".join(res)

if __name__ == "__main__":
    g = Results("shendrickson@gnip.com"
            , "XXXXXPASSWORDXXXXX"
            , "https://gnip-api.twitter.com/search/30day/accounts/shendrickson/wayback.json")
    #list(g.get_time_series(pt_filter="bieber", count_bucket="hour"))
    print(g)
    print( list(g.get_activities(pt_filter="bieber", max_results = 10)) )
    print( list(g.get_geo(pt_filter = "bieber has:geo", max_results = 10)) )
    print( list(g.get_time_series(pt_filter="beiber", count_bucket="hour")) )
    print( list(g.get_top_links(pt_filter="beiber", max_results=100, n=30)) )
    print( list(g.get_top_users(pt_filter="beiber", max_results=100, n=30)) )
    print( list(g.get_top_grams(pt_filter="bieber", max_results=100, n=50)) )
    print( list(g.get_frequency_items(10)) )
    print(g)
    print(g.get_rate())
    g.execute(pt_filter="bieber", query=True)
