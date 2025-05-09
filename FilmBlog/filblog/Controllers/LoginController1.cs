using Microsoft.AspNetCore.Mvc;
using filblog.Models;
using System.Collections.Generic;
using System.Linq;

namespace filblog.Controllers
{
    public class LoginController : Controller
    {
        
        private static List<User> users = new List<User>
        {
            new User { Id = 1, Name = "nizar", Email = "john@example.com", Password = "123456" },
            new User { Id = 2, Name = "Jane Doe", Email = "jane@example.com", Password = "password" }
        };
        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }
        [HttpPost]
        public IActionResult Index(User model)
        {
            var user = users.FirstOrDefault(u => u.Name == model.Name && u.Password == model.Password);
            
            if (user != null)
            {
                return RedirectToAction("Index", "Home");
                
            }
            else
            {
                ViewBag.ErrorMessage = "Geçersiz kullanıcı adı veya şifre.";
                return View();
            }
        }
        [HttpGet]
        public IActionResult Register()
        {
            return View();
        }
        [HttpPost]
        [HttpPost]
        public IActionResult Register(User model)
        {
            if (users.Any(u => u.Name == model.Name))
            {
                ViewBag.RegisterErrorMessage = "Bu kullanıcı adı zaten kullanılmış.";
                return View();
            }
            if (users.Any(u => u.Email == model.Email))
            {
                ViewBag.RegisterErrorMessage = "Bu e-posta adresi zaten kullanılmış.";
                return View();
            }

            var newUser = new User
            {
                Id = users.Count + 1,
                Name = model.Name,
                Email = model.Email,
                Password = model.Password
            };

            users.Add(newUser);
            return RedirectToAction("Index", "Home");
        }
    }
}
