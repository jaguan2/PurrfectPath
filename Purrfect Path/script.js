let username = "", len;
let success = 0;

/* password requirements
 * - have at least 8 characters
 * - have at least 1 uppercase character
 * - have at least 1 number
*/

function validation (username) {
    len = username.length;
    if (len < 8) {
        success = 1;
        return;
    } else if (username != username.toLowerCase()) {
        success = 1;
        return;
    } else if (/\d/.test(str) == false) {
        success = 1;
        return;
    }
}

if (success == 1)
    console.log("Password Failed.");

validation();