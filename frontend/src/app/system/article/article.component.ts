import { Component, Input, OnInit } from '@angular/core';
import { PostModel } from 'src/app/shared/models/PostModel';
import { PostService } from 'src/app/shared/services/post.service';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css'],
})
export class ArticleComponent implements OnInit {
  @Input() post: PostModel | null = null;
  constructor(private postService: PostService) {}
  ckeditorContent: string = '';
  ngOnInit(): void {
    if (this.post)
      this.postService
        .GetContentByName(this.post.url_content)
        .subscribe((response) => {
          this.ckeditorContent = response as string;
        });
  }
  public editorConfigDisplay = {
    toolbar: [],
  };
}
