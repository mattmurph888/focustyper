/**
 * When key press
 * only tracks alphanumeric keys
 */
let text_box = document.getElementById('play-text');
let letters = text_box.children;
let cur_char_index = 0;
let guessed = false;
let update_speed_var;
let clock_var;
let num_key_presses = 0;
letters[cur_char_index].style.boxShadow = '0px 1px 5px rgb(126, 126, 126)';
document.addEventListener(
	'keypress',
	(event) => {
		let name = event.key;
		let code = event.code;

        // if you have not finished the level
		if (cur_char_index < letters.length) {


			// take away the previous wrong letter overlay
			letters[cur_char_index].style.setProperty('--letter_opacity', '0');

			// when you type the correct letter
			if (name == letters[cur_char_index].innerHTML) {
                // start the timer if it has not already
                if (!time_started) {
                    update_displays_var = setInterval(updateDisplays, 1000);
                    clock_var = setInterval(clock, 100);
                    time_started = true;
                }

				// change the color of the guessed letter
				if (guessed) {
					letters[cur_char_index].style.backgroundColor = 'rgba(200,200,0,0.5)';
				} else {
					letters[cur_char_index].style.backgroundColor = 'rgba(0,200,0,0.5)';
				}

				// reset the box shadow on guessed letters
				letters[cur_char_index].style.boxShadow = '';

				// move the text box to the left
				text_box.style.transform = `translateX(-${cur_char_index + 1}em)`;

				// increment to the next leter
				cur_char_index += 1;

                // if we have reached the end of the text, turn off the timer
                if (cur_char_index >= letters.length) {
                    num_key_presses += 1; // need +1 for correct accuracy
                    updateDisplays();
                    clearInterval(update_displays_var);
                    clearInterval(clock_var);
                    setTimeout(customSubmit, 2000);
                }

				// update the box shadow to the right letter only if not at the end
				if (cur_char_index < letters.length) {
					letters[cur_char_index].style.boxShadow =
						'0px 3px 5px rgb(126, 126, 126)';
				}

				// reset guessed for the next letter
				guessed = false;
			} else {
				// else you have typed the wrong letter
				// overlays the wrong letter being pressed
				letters[cur_char_index].style.setProperty('--content', `"${name}"`);
				letters[cur_char_index].style.setProperty('--letter_opacity', '1');

				// set to true so that the letter turns yellow instead of green
				guessed = true;
			}
		} 

        // increment the number of key presses
        if (time_started) {
            num_key_presses += 1;
        }
	},
	false
);

/**
 * When key up
 */
document.addEventListener('keyup', (event) => {
	if (cur_char_index < letters.length) {
		// if you are not done with the lesson
		// remove the wrong letter overlay
		letters[cur_char_index].style.setProperty('--letter_opacity', '0');
	}
});


/**
 * displays data from the current lesson being played
 */
time_started = false;
function updateDisplays() {
    // calculate and display the current speed in wpm
    let cur_speed = parseInt((cur_char_index/5) / (cur_time/60));
    document.getElementById('speed').innerHTML = cur_speed;

    // calculate and display the current accuracy percentage
    let cur_accuracy = parseInt(cur_char_index / num_key_presses * 100);
    document.getElementById('accuracy').innerHTML = cur_accuracy;
}

/**
 * runs the clock
 */
cur_time = 0
function clock() {
    cur_time += 0.1;
 }

// submits a hidden form on the play.html page
// using the hidden form allows django to process the post in the recap view
function customSubmit() {

    console.log(document.getElementsByName('speed').value);
    try {
        document.getElementsByName('speed')[0].value = document.getElementById('speed').innerText;
        document.getElementsByName('accuracy')[0].value = document.getElementById('accuracy').innerText;
        document.getElementsByName('focus')[0].value = document.getElementById('focus').innerText;
    } catch {
        
    }
    let play_form = document.getElementById('play-form');
    play_form.submit()
}

