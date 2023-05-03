let text_box = document.getElementById('play-text'); 	// box that wraps the level text
let letters = text_box.children; 						// array of the individual letter elements
let cur_char_index = 0;									// index of the current letter being typed
let guessed = false;									// have you made a key press at the current key	
let update_displays_var;								// setInterval variable for updating state displays
let clock_var = setInterval(clock, 100);				// updates the clock
let cur_time = 0;										// keeps how much time has passed in tenths of seconds
let num_key_presses = 0;								// total number of key presses. Starts counting with the first correct key press
let box_shadow = '0px 0px 5px 2px rgb(126, 126, 126)';	// box shadow that goes around the current letter
let time_started = false;								// have you guessed the first letter correctly

letters[cur_char_index].style.boxShadow = box_shadow;	// set the cur letter with the box shadow
letters[cur_char_index].style.zIndex = '2';				// make sure the cur letter is in the front

/**
 * When key press
 * only tracks alphanumeric keys
 */
document.addEventListener(
	'keypress',
	(event) => {
		let name = event.key;

		// if you have not finished the level
		if (cur_char_index < letters.length) {
			// take away the previous wrong letter overlay
			letters[cur_char_index].style.setProperty('--letter_opacity', '0');

			// when you type the correct letter
			if (name == letters[cur_char_index].innerHTML) {

				// start the timer if it has not already
				if (!time_started) {
					update_displays_var = setInterval(updateDisplays, 1000);
					cur_time = 0;
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
				letters[cur_char_index].style.zIndex = '1';

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
					letters[cur_char_index].style.zIndex = '2';
					letters[cur_char_index].style.boxShadow = box_shadow;
				}

				// reset guessed for the next letter
				guessed = false;
			} else {
				// else you have typed the wrong letter
				// overlays the wrong letter being pressed
				letters[cur_char_index].style.setProperty('--content', `"${name}"`);
				letters[cur_char_index].style.setProperty('--letter_opacity', '1');

				// set to true so that the letter turns yellow instead of green
				if (time_started) {
					guessed = true;
				}
				
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
	// if you are not done with the lesson
	if (cur_char_index < letters.length) {
		// remove the wrong letter overlay
		letters[cur_char_index].style.setProperty('--letter_opacity', '0');
	}
});


/**
 * displays data from the current lesson being played
 */
function updateDisplays() {
	// calculate and display the current speed in wpm
	let cur_speed = parseInt(cur_char_index / 5 / (cur_time / 60));
	document.getElementById('speed').innerHTML = cur_speed;

	// calculate and display the current accuracy percentage
	let cur_accuracy = parseInt((cur_char_index / num_key_presses) * 100);
	document.getElementById('accuracy').innerHTML = cur_accuracy;
}

/**
 * runs the clock
 */
function clock() {
	cur_time += 0.1; // time is kept in tenths of seconds
}


/**
 * submits a hidden form on the play.html page
 * using the hidden form allows django to process the post in the recap view
 */
function customSubmit() {
	console.log(document.getElementsByName('speed').value);
	try {
		document.getElementsByName('speed')[0].value = document.getElementById('speed').innerText;
		document.getElementsByName('accuracy')[0].value = document.getElementById('accuracy').innerText;
	} catch {}

	let play_form = document.getElementById('play-form');
	play_form.submit();
}
