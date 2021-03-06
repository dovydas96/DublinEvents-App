package ie.dcu.mail.dublinevents;

import android.content.Context;
import android.content.Intent;
import android.support.design.widget.TabLayout;
import android.support.v7.app.AppCompatActivity;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.os.Bundle;


public class Main2Activity extends AppCompatActivity {



    private SectionsPagerAdapter mSectionsPagerAdapter;
    private ViewPager mViewPager;
    public static Context mContext;
    public SqliteDBHandler dbHandler;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        mContext = getApplicationContext();

        dbHandler = new SqliteDBHandler(this, null, null, 14);
        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
        mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager());

        // Set up the ViewPager with the sections adapter.
        mViewPager = findViewById(R.id.container);
        mViewPager.setAdapter(mSectionsPagerAdapter);

        //Limit page load to 4
        mViewPager.setOffscreenPageLimit(4);
        //Find
        TabLayout tabLayout = findViewById(R.id.tabs);
        mViewPager.addOnPageChangeListener(new TabLayout.TabLayoutOnPageChangeListener(tabLayout));
        tabLayout.addOnTabSelectedListener(new TabLayout.ViewPagerOnTabSelectedListener(mViewPager));

    }



    /**
     * A {@link FragmentPagerAdapter} that returns a fragment corresponding to
     * one of the sections/tabs/pages.
     */
    public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            // getItem is called to instantiate the fragment for the given page.
            switch (position){
                case 0:
                    TableEvents events = new TableEvents();
                    return events;
                case 1:
                    TablePub pub = new TablePub();
                    return pub;
                case 2:
                    TableVenues venues = new TableVenues();
                    return venues;
                case 3:
                    FavFragment fav = new FavFragment();
                    return fav;
                default:
                    return null;
            }
        }

        @Override
        public int getCount() {
            // Show 4 total pages.
            return 4;
        }

        @Override
        public CharSequence getPageTitle(int position){

            switch (position){

                case 0:
                    return "Events";
                case 1:
                    return "Pubs";
                case 2:
                    return "Venues";
                case 3:
                    return "Favourites";
            }
            return null;
        }

    }


    public static Context getContext() {
        return mContext;
    }

}


