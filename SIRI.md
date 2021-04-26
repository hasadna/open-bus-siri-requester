# SIRI

Documentation regarding the source SIRI data

## sources

* https://www.gov.il/he/Departments/General/real_time_information_siri
* https://www.gov.il/BlobFolder/generalpage/real_time_information_siri/he/ICD_SM_28_31.pdf

## SIRI Snapshot request

This is the relevant documentation regarding the SIRI snapshot request we are making

* 7.15.MonitoringRef=AllActiveTripsFilter with StopMonitoringDetailLevel=normal:
  * 7.15.1. The Response will contains details about all the Vehicles that
    are in an Active trip.
  * 7.15.2. An Active starts when the Vehicle is at the origin stop, till it
    reaches the destination stop.
  * 7.15.3. The Response will contains details about the trip, the Vehicle
    position, but no prediction is contained.
  * 7.15.4. The Data Center generate a Response for this filter every 15
    seconds, and the Developer gets the latest, and most updated
    Response for this filter.
  * 7.15.5. This filter resemble the 'vehicle positions' at the GTFSRealtime, but at a different format.
  * 7.15.6. This filter is a 'snapshot'. See more details about snapshot at
    section 7.18.

* 7.18
  * 7.18.1. The Response will contains a series of MonitoredStopVisit
    entities.
  * 7.18.2. A Developer can send a Request with that filter at rate of 15
    seconds or more between each Request.
  * 7.18.3. When this filter is used, the Request should NOT contain
    parameters for: PreviewInterval, StartTime, LineRef,
    MaximumStopVisits, MaximumStopVisitsPerLine,
    MaximumNumberOfCallsOnwards.
  * 7.18.4. The Request can be just for json format. XML format is not
    supported.
  * 7.18.5. The following table summarize the fields that will be included
    in the Response:
    * RecordedAtTime
    * LineRef
    * FramedVehicleJourneyRef
    * OperatorRef
    * OriginAimedDepartureTime
    * VehicleLocation
    * Bearing
    * Velocity
    * VehicleRef
    * MonitoredCall
    * MonitoredCall.StopPointRef
    * MonitoredCall.Order
    * MonitoredCall.DistanceFromStop
