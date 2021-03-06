package ie.dcu.mail.dublinevents;


import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.PorterDuff;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ExpandableListView;
import android.widget.Spinner;
import android.widget.Toast;


public class TablePub extends Fragment implements LocationListener {

    LocationManager locationManager;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.pub_frag, container, false);

        final ExpandableListView expandbleLis = rootView.findViewById(R.id.pubFragView);
        expandbleLis.setDividerHeight(2);
        expandbleLis.setGroupIndicator(null);
        expandbleLis.setClickable(true);

        if (ContextCompat.checkSelfPermission(getContext(), android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getContext(), android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(getActivity(), new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION, android.Manifest.permission.ACCESS_COARSE_LOCATION}, 101);
        }

        Toolbar toolbar = rootView.findViewById(R.id.pub_toolbar);
        ((AppCompatActivity)getActivity()).setSupportActionBar(toolbar);
        ((AppCompatActivity)getActivity()).getSupportActionBar().setTitle("SORT BY");

        Spinner spinner = rootView.findViewById(R.id.PubSpinner);
        spinner.getBackground().setColorFilter(getResources().getColor(R.color.white), PorterDuff.Mode.SRC_ATOP);

        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {


                if (parentView.getItemAtPosition(position).toString().equals("Name")) {
                    Downloader d = new Downloader(getActivity(), "http://159.65.84.145/connt.php"+
                            "?table=venuesTest&where=category =" +
                            "&category=Pub&order=name&display=ASC", expandbleLis, "venue");
                    d.execute();
                }

                if (parentView.getItemAtPosition(position).toString().equals("Rating")) {
                    Downloader d = new Downloader(getActivity(), "http://159.65.84.145/connt.php"
                            + "?table=venuesTest&where=category =" +
                            "&category=Pub&order=rating&display=DESC", expandbleLis, "venue");
                    d.execute();
                }

                if (parentView.getItemAtPosition(position).toString().equals("Location")) {
                    getLocation();
                }

                if (parentView.getItemAtPosition(position).toString().equals("Search Pubs")) {
                    String message="pub";
                    Intent intent = new Intent(getActivity(),SearchActivity.class);
                    intent.putExtra("message",message);
                    startActivity(intent);
                }

            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
                // Do nothing
            }

        });
        return rootView;
    }

    void getLocation() {
        try {
            locationManager = (LocationManager) getActivity().getSystemService(Context.LOCATION_SERVICE);
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 5000, 5, this);
        }
        catch(SecurityException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onLocationChanged(Location location) {
        final ExpandableListView expandbleLis = getActivity().findViewById(R.id.pubFragView);
        expandbleLis.setDividerHeight(2);
        expandbleLis.setGroupIndicator(null);
        expandbleLis.setClickable(true);
        Downloader d = new Downloader(getActivity(), "http://159.65.84.145/distance.php"
                + "?lat="+location.getLatitude()+"&where= = &category=Pub&long="+location.getLongitude(), expandbleLis, "venue");
        d.execute();
    }

    @Override
    public void onProviderDisabled(String provider) {
        Toast.makeText(getActivity(), "Please Enable GPS and Internet", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {

    }
}
