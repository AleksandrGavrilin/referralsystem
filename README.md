
# <span style='color:rgb(67, 89, 97)'>Referral system (with interface for testing).</span>

### <span style='color:rgb(67, 89, 97)'>Key Features:</span>

\- authorization by phone number; <br />
\- record a new user in the database; <br />
\- assigning a generated code to a new user; <br />
\- the ability to track in the profile the number of users who entered the invite code of the current user. <br />

### <span style='color:rgb(67, 89, 97)'>Description of main functions (in the "views" file):</span>


**The function "phone_auth" sending an authorization code, adding a user (phone number) to the database.** <br />
Below are the main parameters: <br />

Endpoint: api/phone_auth <br />
method: GET <br />
params: phonenumber <br />
answer: OK, error(403) <br />

**The function "phone_code" sending an invite code, adding a user (phone number, invitation code) to the "User" database.** <br />
Below are the main parameters: <br />

Endpoint: api/phone_code <br />
method: GET <br />
params: phonenumber, phonecode <br />
answer: OK/JSON(referralcode), error(403) <br />

**The function "invite" processes the received invite code.** <br />
Below are the main parameters: <br />

Endpoint: api/invite <br />
method: GET <br />
params: phonenumber, usercode, invitecode <br />
answer: OK, error(401) <br />

**The function "getreferrals" provides a list of invited users.** <br />
Below are the main parameters: <br />

Endpoint: api/getreferrals <br />
method: GET <br />
params: phonenumber, usercode <br />
answer: OK/JSON(phonelist), error(401) <br />


### <span style='color:rgb(67, 89, 97)'>System testing. </span>
To test the system, run the file "testapi.py" and follow the instructions. <br />

