import { LitElement, html } from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';
import 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js';
import 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js';

class KatexElement extends LitElement {
  static properties = {
    content: { type: String },
  };

  updated() {
    this.renderMath();
  }

  renderMath() {
    if (this.content) {
      this.shadowRoot.innerHTML = this.content;
      renderMathInElement(this.shadowRoot, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false },
        ],
      });
    }
  }

  render() {
    return html`<div></div>`;
  }
}

customElements.define('katex-element', KatexElement);