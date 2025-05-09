    using filblog.Models;
    using Microsoft.AspNetCore.Mvc;
    using System.Diagnostics;

    namespace filblog.Controllers
    {
        public class HomeController : Controller
        {
            List<Blog> blogPosts = new List<Blog>
            {
                new Blog
                {
                    Id = 1,
                    Title = "Kara Şövalye",
                    Content = "    Lorem ipsum dolor sit amet consectetur adipisicing elit. \r\n    Repellat dolorem dolore nesciunt, quibusdam fugiat reprehenderit ad odio officiis reiciendis aut, aliquam dignissimos doloremque ullam odit dicta facere amet obcaecati excepturi recusandae ab! \r\n    Nihil, iste? Non quae commodi maiores illo enim! Sapiente eos sit sequi accusantium esse dolores dicta, illo quas!",
                    Thumbnail ="~/filmblog.templete/img/filmfotolar/Kara Şövalye (2008).jpg",
                    img1="~/filmblog.templete/img/filmhakkında/karasovalye1.jpg",
                    img2="~/filmblog.templete/img/filmhakkında/karasovalye2.jpg",
                    img3="~/filmblog.templete/img/filmhakkında/karasovalye3.jpg",
                },
                new Blog
                {
                    Id = 2,
                    Title = "Barbie",
                    Content = "    Lorem ipsumBARBİEEEEEEEEor sit amet consectetur adipisicing elit. \r\n    Repellat dolorem dolore nesciunt, quibusdam fugiat reprehenderit ad odio officiis reiciendis aut, aliquam dignissimos doloremque ullam odit dicta facere amet obcaecati excepturi recusandae ab! \r\n    Nihil, iste? Non quae commodi maiores illo enim! Sapiente eos sit sequi accusantium esse dolores dicta, illo quas!",
                    Thumbnail = "~/filmblog.templete/img/filmfotolar/Barbie (2023).jpg",
                    img1="~/filmblog.templete/img/filmhakkında/barbie1.jpg",
                    img2="~/filmblog.templete/img/filmhakkında/barbie2.jpg",
                    img3="~/filmblog.templete/img/filmhakkında/barbie3.jpg",
                },
                new Blog
                {
                    Id = 3,
                    Title = "Dövüş Kulubü",
                    Content = "    Lorem ipsum dolor sit amet consectetur adipisicing elit. \r\n    Repellat dolorem dolore nesciunt, quibusdam fugiat reprehenderit ad odio officiis reiciendis aut, aliquam dignissimos doloremque ullam odit dicta facere amet obcaecati excepturi recusandae ab! \r\n    Nihil, iste? Non quae commodi maiores illo enim! Sapiente eos sit sequi accusantium esse dolores dicta, illo quas!",
                    Thumbnail = "~/filmblog.templete/img/filmfotolar/Dövüş Kulübü (1999).jpg",
                    img1="~/filmblog.templete/img/filmhakkında/fight1.jpg",
                    img2="~/filmblog.templete/img/filmhakkında/fight2.jpg",
                    img3="~/filmblog.templete/img/filmhakkında/fight3.jpg",
                },
                new Blog
                {
                    Id = 4,
                    Title = "Esaretin Bedeli",
                    Content = "    Lorem ipsum dolor sit amet consectetur adipisicing elit. \r\n    Repellat dolorem dolore nesciunt, quibusdam fugiat reprehenderit ad odio officiis reiciendis aut, aliquam dignissimos doloremque ullam odit dicta facere amet obcaecati excepturi recusandae ab! \r\n    Nihil, iste? Non quae commodi maiores illo enim! Sapiente eos sit sequi accusantium esse dolores dicta, illo quas!",
                    Thumbnail = "~/filmblog.templete/img/filmfotolar/Esaretin Bedeli (1994).jpg",
                    img1="~/filmblog.templete/img/filmhakkında/esaret1.jpg",
                    img2="~/filmblog.templete/img/filmhakkında/esaret2.jpg",
                    img3="~/filmblog.templete/img/filmhakkında/esaret3.jpg",
                },
                new Blog
                {
                    Id = 5,
                    Title = "Forrest Gump",
                    Content = "    Lorem ipsum dolor sit amet consectetur adipisicing elit. \r\n    Repellat dolorem dolore nesciunt, quibusdam fugiat reprehenderit ad odio officiis reiciendis aut, aliquam dignissimos doloremque ullam odit dicta facere amet obcaecati excepturi recusandae ab! \r\n    Nihil, iste? Non quae commodi maiores illo enim! Sapiente eos sit sequi accusantium esse dolores dicta, illo quas!",
                    Thumbnail = "~/filmblog.templete/img/filmfotolar/Forrest Gump (1994).jpg",
                    img1="~/filmblog.templete/img/filmhakkında/forrest1.jpg",
                    img2="~/filmblog.templete/img/filmhakkında/forrest2.jpg",
                    img3="~/filmblog.templete/img/filmhakkında/forrest3.jpg",
                },
                new Blog
                {
                    Id = 6,
                    Title = "Orumcek Adam Eve Dönüş Yok",
                    Content = "    Lorem ipsum dolor sit amet consectetur adipisicing elit. \r\n    Repellat dolorem dolore nesciunt, quibusdam fugiat reprehenderit ad odio officiis reiciendis aut, aliquam dignissimos doloremque ullam odit dicta facere amet obcaecati excepturi recusandae ab! \r\n    Nihil, iste? Non quae commodi maiores illo enim! Sapiente eos sit sequi accusantium esse dolores dicta, illo quas!",
                    Thumbnail = "~/filmblog.templete/img/filmfotolar/Örümcek Adam_ Eve Dönüş Yok (2021).jpg",
                    img1="~/filmblog.templete/img/filmhakkında/örümcek1.jpg",
                    img2="~/filmblog.templete/img/filmhakkında/örümcek2.jpg",
                    img3="~/filmblog.templete/img/filmhakkında/örümcek3.jpg",
                },
            };
            public ActionResult Index()
            {
           
                return View(blogPosts);
            }
            public ActionResult Detail(int id)
            {
                Blog selectedBlog = blogPosts.FirstOrDefault(blog => blog.Id == id);

                if (selectedBlog == null)
                {
                    return RedirectToAction("Index");
                }
                return View(selectedBlog);
            }
    }
    }