import { Component } from '@angular/core';
import { WordContextService } from './word-context.service';

@Component({
  selector: 'app-word-context',
  templateUrl: './word-context.component.html',
  styleUrls: ['./word-context.component.css']
})
export class WordContextComponent {
  model = { word: '', context: '' };

  constructor(private service: WordContextService) {}

  onSubmit(): void {
    this.service.postWordWithContext(this.model.word, this.model.context).subscribe({
      next: (response) => console.log(response),
      error: (error) => console.error(error)
    });
  }
}